# System Nexa 2 – Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/)

Integration för att styra **System Nexa 2**-enheter direkt i Home Assistant via det lokala API:t.

## ✨ Funktioner
- Stöd för flera modeller:
  - **Dimmer (light)**: WPD-01, WBD-01
  - **På/av (switch)**: WPR-01, WPO-01, WBR-01
- Live-status via WebSocket
- Styrning via WebSocket (fallback till HTTP)
- Dimning 0–100 % (avrundning till 2 decimaler)
- Config Flow (GUI) med host, port, token och modellval
- DeviceInfo (tillverkare, modell, config-url)
- Migration av gamla entries → inga manuella borttagningar

## 📦 Installation
1. Lägg till detta repo som *custom repository* i HACS  
2. Installera “System Nexa 2” integrationen  
3. Starta om Home Assistant  
4. Lägg till integrationen via Inställningar → Enheter & tjänster  
5. Ange host/IP, port (default 3000), ev. token och modelltyp

## 🔧 Konfiguration
Alla inställningar sker via Home Assistants UI (Config Flow).  
Om du vill ändra enhetens område kan detta göras i HA:s enhetsvyer.

## 🛠 Support
Detta projekt är community-drivet och inte officiellt från Nexa.
