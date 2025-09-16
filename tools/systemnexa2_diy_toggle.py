# 1) Aktivera DIY (stänger av molnet)
python systemnexa2_diy_toggle.py --host 192.168.1.55 --enable

# Med token (om din enhet kräver det)
python systemnexa2_diy_toggle.py --host 192.168.1.55 --token DIN_TOKEN --enable

# 2) Avaktivera DIY (slå på moln igen)
python systemnexa2_diy_toggle.py --host 192.168.1.55 --disable

# 3) Aktivera DIY + skriv config-snutt för HA
python systemnexa2_diy_toggle.py --host 192.168.1.55 --enable --write-config ./systemnexa2_config.json
