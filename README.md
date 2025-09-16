
# Home Assistant – System Nexa 2 (DIY)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)  
![version](https://img.shields.io/badge/version-v0.1.0-blue)  
![license](https://img.shields.io/github/license/YOURNAME/homeassistant-systemnexa2)

Custom integration for [Home Assistant](https://www.home-assistant.io/) that lets you control **System Nexa 2** devices in **DIY mode** directly over the local HTTP API – no cloud and no Nexa Bridge X required.

---

## ✨ Features
- Local control of **WPD-01** Wi-Fi dimmer plug  
- Exposes as a standard **light entity** with brightness (0–255)  
- Simple setup via Config Flow (IP, optional token, poll interval)  
- Works fully offline in DIY mode (cloud/app disabled)  

---

## 🔌 Supported devices
- **WPD-01** (Wi-Fi dimmer plug)  

> More devices may work if they expose the same `/state` API – feel free to test and report back.

---

## 🚫 Not required
- ❌ Nexa Bridge X  
- ❌ Nexa cloud / app  

This integration talks **directly** to the device over HTTP.

---

## 📦 Installation

### Option A – HACS (Custom Repository)
1. Go to **HACS → Integrations → 3-dot menu → Custom repositories**.  
2. Add your repo URL, e.g.  
   ```
   https://github.com/YOURNAME/homeassistant-systemnexa2
   ```
   Category: **Integration**.  
3. Install **System Nexa 2** from HACS.  
4. Restart Home Assistant.  
5. Add the integration:  
   **Settings → Devices & services → Add integration → System Nexa 2**.  

### Option B – Manual
1. Download the latest [release ZIP](https://github.com/YOURNAME/homeassistant-systemnexa2/releases).  
2. Extract into:  
   ```
   config/custom_components/systemnexa2/
   ```  
3. Restart Home Assistant.  
4. Add the integration via **Settings → Devices & services**.  

---

## ⚙️ Configuration
When adding the integration, you’ll be asked for:
- **Host** → IP or hostname of your System Nexa 2 device  
- **Token** → leave empty unless your device requires it  
- **Poll interval** → seconds between state updates (default: 10)  
- **Name** → optional friendly name (default: WPD-01)  

---

## 🖥️ Usage
Once configured, a new **light entity** will appear in Home Assistant, e.g.:

```
light.wpd_01
```

- **On/Off** → `GET /state?on=1|0`  
- **Brightness** → `GET /state?v=0.0–1.0` (mapped to 0–255 in HA)  
- **State** → `GET /state` (returns JSON with fields like `on` and `v`)  

---
## Port
- You can enter **host** as `192.168.x.x` and choose a **Port** (default suggested: `3000`).  
- If you already put `host:port` in the host field, the **Port** field is ignored.

Typical endpoints:
- `GET /state` (JSON)
- `GET /state?on=1|0`
- `GET /state?v=0.0–1.0`

---

## 📸 Screenshots
Add your own screenshots here to show integration setup and the entity in HA UI.

![screenshot-add-integration](docs/screenshot-add-integration.png)  
![screenshot-light-entity](docs/screenshot-light-entity.png)  

---

## 🛠️ Development
- API docs: [System Nexa 2 DIY API](https://docs.systemnexa2.se/api/)  
- Tested with: Home Assistant 2025.1+  
- Contributions welcome: pull requests, issues, feature requests!  

---

---

## 🔧 Tools

This repository also includes helper scripts in the [`tools/`](tools) folder.

### `systemnexa2_diy_toggle.py`
Small Python utility to **enable/disable DIY mode** on a System Nexa 2 device and (optionally) generate a Home Assistant config snippet.

#### Usage examples

```bash
# Enable DIY (disable cloud)
python tools/systemnexa2_diy_toggle.py --host 192.168.1.55 --enable

# Enable DIY with token header
python tools/systemnexa2_diy_toggle.py --host 192.168.1.55 --token YOURTOKEN --enable

# Disable DIY (re-enable cloud mode)
python tools/systemnexa2_diy_toggle.py --host 192.168.1.55 --disable

# Enable DIY and write config snippet for HA integration
python tools/systemnexa2_diy_toggle.py --host 192.168.1.55 --enable --write-config ./systemnexa2_config.json

---

## 📜 License
[MIT](LICENSE) © 2025 YOUR NAME
