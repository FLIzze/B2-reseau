- [x] carte réseau host-only avec IP statique
- [x] pas de carte NAT, sauf si demandée
- [x] connexion SSH fonctionnelle
- [x] firewall actif
- [x] SELinux désactivé
- [x] hostname défini

## Compte-rendu

☀️ Sur **`node1.lan1.tp2`**

- afficher ses cartes réseau

`[abel@node1 ~]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:2a:1c:f0 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.11/24 brd 10.1.1.255 scope global noprefixroute enp0s3
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe2a:1cf0/64 scope link 
       valid_lft forever preferred_lft forever
`

- afficher sa table de routage

[abel@node1 ~]$ ip r s
10.1.1.0/24 dev enp0s3 proto kernel scope link src 10.1.1.11 metric 100 
10.1.2.0/24 via 10.1.1.254 dev enp0s3 proto static metric 100 

- prouvez qu'il peut joindre `node2.lan2.tp2`

`[abel@node1 ~]$ ping node2.lan2
PING node2.lan2 (10.1.2.12) 56(84) bytes of data.
64 bytes from node2.lan2 (10.1.2.12): icmp_seq=1 ttl=63 time=0.637 ms
`

- prouvez avec un `traceroute` que le paquet passe bien par `router.tp2`

`[abel@node1 ~]$ traceroute node2.lan2
traceroute to node2.lan2 (10.1.2.12), 30 hops max, 60 byte packets
 1  routeur.lan1 (10.1.1.254)  0.455 ms  0.457 ms  0.449 ms
 2  node2.lan2 (10.1.2.12)  0.966 ms !X  0.947 ms !X  0.938 ms !X
`
# II. Interlude accès internet

☀️ **Sur `router.tp2`**

- prouvez que vous avez un accès internet (ping d'une IP publique)

`[abel@router ~]$ ping 142.250.201.174
PING 142.250.201.174 (142.250.201.174) 56(84) bytes of data.
64 bytes from 142.250.201.174: icmp_seq=1 ttl=63 time=56.2 ms
`

- prouvez que vous pouvez résoudre des noms publics (ping d'un nom de domaine public)

`[abel@router ~]$ ping google.com
PING google.com (172.217.20.206) 56(84) bytes of data.
64 bytes from par10s50-in-f14.1e100.net (172.217.20.206): icmp_seq=1 ttl=63 time=23.5 ms
`

☀️ **Accès internet LAN1 et LAN2**

- ajoutez une route par défaut sur les deux machines du LAN1

```bash
[abel@node1 ~]$ cat /etc/sysconfig/network-scripts/ifcfg-enp0s3 | grep GATEWAY
GATEWAY=10.1.1.254
```

- ajoutez une route par défaut sur les deux machines du LAN2

```bash
[abel@node1 ~]$ cat /etc/sysconfig/network-scripts/ifcfg-enp0s8 | grep GATEWAY
GATEWAY=10.1.2.254
```

- configurez l'adresse d'un serveur DNS que vos machines peuvent utiliser pour résoudre des noms

```bash
[abel@node1 ~]$ sudo cat /etc/resolv.conf | grep nameserver
nameserver 1.1.1.1
```

- dans le compte-rendu, mettez-moi que la conf des points précédents sur `node2.lan1.tp2`
- prouvez que `node2.lan1.tp2` a un accès internet :
  - il peut ping une IP publique

```bash
[abel@node2 ~]$ ping 142.250.201.174
PING 142.250.201.174 (142.250.201.174) 56(84) bytes of data.
64 bytes from 142.250.201.174: icmp_seq=1 ttl=61 time=25.5 ms
```

  - il peut ping un nom de domaine public

```bash
[abel@node2 ~]$ ping google.com
PING google.com (172.217.20.174) 56(84) bytes of data.
64 bytes from par10s49-in-f14.1e100.net (172.217.20.174): icmp_seq=1 ttl=61 time=23.7 ms
```

# III. Services réseau

## 1. DHCP

☀️ **Sur `dhcp.lan1.tp2`**

- n'oubliez pas de renommer la machine (`node2.lan1.tp2` devient `dhcp.lan1.tp2`)

```bash
[abel@dhcp ~]$ hostname
dhcp.lan1.tp2
```

- changez son adresse IP en `10.1.1.253`

```bash
[abel@dhcp ~]$ ip a | grep enp0s3
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    inet 10.1.1.253/24 brd 10.1.1.255 scope global noprefixroute enp0s3
```

- setup du serveur DHCP
  - commande d'installation du paquet

`sudo dnf install dhcp-server`

  - fichier de conf

```bash
sudo cat /etc/dhcp/dhcpd.conf
[sudo] password for abel: 
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd.conf.example
#   see dhcpd.conf(5) man page


default-lease-time 600;
max-lease-time 7200;

authoritative;

subnet 10.1.1.0 netmask 255.255.255.0 {
	range 10.1.1.100 10.1.1.200;
	option routers 10.1.1.254;
	option domain-name-servers 1.1.1.1;
}
```

  - service actif

```bash
[abel@dhcp ~]$ sudo systemctl status dhcpd
● dhcpd.service - DHCPv4 Server Daemon
     Loaded: loaded (/usr/lib/systemd/system/dhcpd.service; enabled; preset: disabled)
     Active: active (running) since Fri 2023-11-03 17:25:32 CET; 59min ago
```

☀️ **Sur `node1.lan1.tp2`**

- demandez une IP au serveur DHCP

`sudo dhclient`

- prouvez que vous avez bien récupéré une IP *via* le DHCP

```bash
[abel@node1 ~]$ sudo tcpdump port 67 and port 68
18:29:47.385042 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from 08:00:27:2a:1c:f0 (oui Unknown), length 300
18:29:48.387214 IP dhcp.bootps > 10.1.1.103.bootpc: BOOTP/DHCP, Reply, length 300
18:29:48.387456 IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from 08:00:27:2a:1c:f0 (oui Unknown), length 300
18:29:48.403609 IP dhcp.bootps > 10.1.1.103.bootpc: BOOTP/DHCP, Reply, length 300
```

- prouvez que vous avez bien récupéré l'IP de la passerelle

```bash
[abel@node1 ~]$ ip r s
default via 10.1.1.254 dev enp0s3 
default via 10.1.1.254 dev enp0s3 proto dhcp src 10.1.1.102 metric 100 
```

- prouvez que vous pouvez `ping node1.lan2.tp2`

```bash
[abel@node1 ~]$ ping node1.lan2
PING node1.lan2 (10.1.2.11) 56(84) bytes of data.
64 bytes from node1.lan2 (10.1.2.11): icmp_seq=1 ttl=63 time=0.571 ms
```

## 2. Web web web


La conf du serveur web :

- ce sera notre vieil ami NGINX
- il écoutera sur le port 80, port standard pour du trafic HTTP
- la racine web doit se trouver dans `/var/www/site_nul/`
  - vous y créerez un fichier `/var/www/site_nul/index.html` avec le contenu de votre choix
- vous ajouterez dans la conf NGINX **un fichier dédié** pour servir le site web nul qui se trouve dans `/var/www/site_nul/`
  - écoute sur le port 80
  - répond au nom `site_nul.tp2`
  - sert le dossier `/var/www/site_nul/`
- n'oubliez pas d'ouvrir le port dans le firewall 🌼

```bash
[abel@web ~]$ sudo firewall-cmd --list-all | grep services
  services: cockpit dhcpv6-client http ssh
```

---

☀️ **Sur `web.lan2.tp2`**

- n'oubliez pas de renommer la machine (`node2.lan2.tp2` devient `web.lan2.tp2`)

```bash
[abel@web ~]$ hostname
web.lan2.tp2
```

- setup du service Web
  - installation de NGINX

`sudo dnf install nginx`

  - gestion de la racine web `/var/www/site_nul/`
  - configuration NGINX

```bash
[abel@web /]$ cat /etc/nginx/nginx.conf
    server {
        listen       80;
        listen       [::]:80;
        server_name  _;
        root         /var/www/site_nul/;
        include /etc/nginx/default.d/*.conf;

        error_page 404 /404.html;
        location = /404.html {
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
        }
```

  - service actif

```bash
sudo systemctl enable nginx

[abel@web /]$ sudo systemctl status nginx
● nginx.service - The nginx HTTP and reverse proxy server
     Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; preset: disabled)
     Active: active (running) since Fri 2023-11-03 17:42:05 CET; 1h 4min ago
```

  - ouverture du port firewall

```bash
[abel@web /]$ sudo firewall-cmd --add-service=http --permanent
success

[abel@web /]$ sudo firewall-cmd --reload
success
```

- prouvez qu'il y a un programme NGINX qui tourne derrière le port 80 de la machine (commande `ss`)

```bash
[abel@web /]$ sudo ss -ltunp | grep 80
tcp   LISTEN 0      511          0.0.0.0:80        0.0.0.0:*    users:(("nginx",pid=11265,fd=6),("nginx",pid=11264,fd=6),("nginx",pid=11200,fd=6))
tcp   LISTEN 0      511             [::]:80           [::]:*    users:(("nginx",pid=11265,fd=7),("nginx",pid=11264,fd=7),("nginx",pid=11200,fd=7))
```

- prouvez que le firewall est bien configuré

```bash
[abel@web /]$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp0s3
  sources: 
  services: cockpit dhcpv6-client http ssh
  ports: 
  protocols: 
  forward: yes
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 
```

☀️ **Sur `node1.lan1.tp2`**

- éditez le fichier `hosts` pour que `site_nul.tp2` pointe vers l'IP de `web.lan2.tp2`

```bash
[abel@web /]$ sudo cat /etc/hosts | grep site
10.1.2.12 site_nul.tp2
```
- visitez le site nul avec une commande `curl` et en utilisant le nom `site_nul.tp2`

```bash
[abel@web /]$ curl site_nul.tp2
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>tp2</title>
</head>

<body>
	bonjour leo
</body>
```


