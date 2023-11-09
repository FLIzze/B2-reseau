import psutil

ipa_dic = (psutil.net_if_addrs())
print(ipa_dic["wlp4s0"][0][1])
