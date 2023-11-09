# TP1 : Maîtrise réseau du poste

- [TP1 : Maîtrise réseau du poste](#tp1--maîtrise-réseau-du-poste)
- [I. Basics](#i-basics)
- [II. Go further](#ii-go-further)
- [III. Le requin](#iii-le-requin)

# I. Basics

> Tout est à faire en ligne de commande, sauf si précision contraire.

☀️ **Carte réseau WiFi**

Déterminer...

- l'adresse MAC de votre carte WiFi

```bash
ip a
14:13:33:d8:37:cb
```

- l'adresse IP de votre carte WiFi

```bash
ip a | grep wlp4s0 
inet 10.33.79.112/20
```

- le masque de sous-réseau du réseau LAN auquel vous êtes connectés en WiFi
- en notation CIDR, par exemple `/16`

`/20`

- ET en notation décimale, par exemple `255.255.0.0`

`255.255.240.0`

---

☀️ **Déso pas déso**

- l'adresse de réseau du LAN auquel vous êtes connectés en WiFi

`10.33.79.*`

- l'adresse de broadcast

`10.33.79.255`

- le nombre d'adresses IP disponibles dans ce réseau

```bash
plage d'adresse: 10.33.64-1 - 10.33.79.254
donc 4 096 adresse
```

---

☀️ **Hostname**

- déterminer le hostname de votre PC

```bash
hostname
flizze
```

---

☀️ **Passerelle du réseau**

Déterminer...

- l'adresse IP de la passerelle du réseau

```bash
ip n s
10.33.79.254
```

- l'adresse MAC de la passerelle du réseau

```bash
7c:5a:1c:d3:d8:76
```

---

☀️ **Serveur DHCP et DNS**

Déterminer...

- l'adresse IP du serveur DHCP qui vous a filé une IP

```bash
cat /var/lib/dhcp/dhclient.leases  | grep dhcp-server-identifier
option dhcp-server-identifier 10.33.79.254;
```

- l'adresse IP du serveur DNS que vous utilisez quand vous allez sur internet

```bash
resolvectl status | grep 'DNS Server'
Current DNS Server: 1.1.1.1
```

---

☀️ **Table de routage**

Déterminer...

- dans votre table de routage, laquelle est la route par défaut

```bash
ip r s
default via 10.33.79.254
```

---

# II. Go further

> Toujours tout en ligne de commande.

---

☀️ **Hosts ?**

- faites en sorte que pour votre PC, le nom `b2.hello.vous` corresponde à l'IP `1.1.1.# 
```bash
cat /etc/hosts | grep 1.1.1.1
1.1.1.1 b2.hello.vous
```

- prouvez avec un `ping b2.hello.vous` que ça ping bien `1.1.1.1`

```bash
ping b2.hello.vous
PING b2.hello.vous (1.1.1.1) 56(84) bytes of data.
64 bytes from b2.hello.vous (1.1.1.1): icmp_seq=1 ttl=57 time=14.2 ms
```

---

☀️ **Go mater une vidéo youtube et déterminer, pendant qu'elle tourne...**

- l'adresse IP du serveur auquel vous êtes connectés pour regarder la vidéo

```bash
ss -tp 
trois serveurs:
34.117.65.55 
142.250.75.226
34.117.237.239
```

- le port du serveur auquel vous êtes connectés

```bash
:https
https donc le port 443
```

- le port que votre PC a ouvert en local pour se connecter au port du serveur distant

```bash
un port par ip 
:32890
:53624
:57014
```
---

☀️ **Requêtes DNS**

Déterminer...

- à quelle adresse IP correspond le nom de domaine `www.ynov.com`

```bash
dig ynov.com
ynov.com.		300	IN	A	104.26.11.233
ynov.com.		300	IN	A	172.67.74.226
ynov.com.		300	IN	A	104.26.10.233
```

- à quel nom de domaine correspond l'IP `174.43.238.89`

```bash
dig -x 174.43.238.89 
89.sub-174-43-238.myvzw.com
```

---

☀️ **Hop hop hop**

Déterminer...

- par combien de machines vos paquets passent quand vous essayez de joindre `www.ynov.com`

```bash
traceroute ynov.com
traceroute to ynov.com (104.26.11.233), 30 hops max, 60 byte packets
 1  _gateway (10.33.79.254)  12.812 ms  12.729 ms  12.694 ms
 2  145.117.7.195.rev.sfr.net (195.7.117.145)  9.383 ms  7.475 ms  7.441 ms
 3  * * *
 4  196.224.65.86.rev.sfr.net (86.65.224.196)  9.180 ms  9.145 ms  9.111 ms
 5  12.148.6.194.rev.sfr.net (194.6.148.12)  17.078 ms 68.150.6.194.rev.sfr.net (194.6.150.68)  17.037 ms  17.005 ms
 6  68.150.6.194.rev.sfr.net (194.6.150.68)  16.973 ms  12.137 ms 12.148.6.194.rev.sfr.net (194.6.148.12)  12.091 ms
 7  141.101.67.48 (141.101.67.48)  10.302 ms  13.307 ms  13.272 ms
 8  172.71.120.4 (172.71.120.4)  13.238 ms 141.101.67.54 (141.101.67.54)  9.784 ms 172.71.120.4 (172.71.120.4)  9.741 ms
 9  104.26.11.233 (104.26.11.233)  9.716 ms  12.532 ms  12.551 ms
```

---

☀️ **IP publique**

Déterminer...

- l'adresse IP publique de la passerelle du réseau (le routeur d'YNOV donc si vous êtes dans les locaux d'YNOV quand vous faites le TP)

```bash
curl ifconfig.me
195.7.117.14
```

---

☀️ **Scan réseau**

Déterminer...

- combien il y a de machines dans le LAN auquel vous êtes connectés

```bash
nmap 10.33.64.0/20
Nmap scan report for 10.33.79.246
Host is up (0.014s latency).
Nmap done: 4096 IP addresses (386 hosts up) scanned in 205.85 seconds
```

# III. Le requin

---

☀️ **Capture ARP**

- 📁 fichier `arp.pcap`
- capturez un échange ARP entre votre PC et la passerelle du réseau

`ip n flush all` pour forcer l'echange arp

> Si vous utilisez un filtre Wireshark pour mieux voir ce trafic, précisez-le moi dans le compte-rendu.

`filtre arp sur Wireshark`

---

☀️ **Capture DNS**

- 📁 fichier `dns.pcap`
- capturez une requête DNS vers le domaine de votre choix et la réponse
- vous effectuerez la requête DNS en ligne de commande

> Si vous utilisez un filtre Wireshark pour mieux voir ce trafic, précisez-le moi dans le compte-rendu.

`filtre dns`
---

☀️ **Capture TCP**

- 📁 fichier `tcp.pcap`
- effectuez une connexion qui sollicite le protocole TCP
- je veux voir dans la capture :
  - un 3-way handshake
  - un peu de trafic
  - la fin de la connexion TCP

> Si vous utilisez un filtre Wireshark pour mieux voir ce trafic, précisez-le moi dans le compte-rendu.

`filtre tcp`
---


