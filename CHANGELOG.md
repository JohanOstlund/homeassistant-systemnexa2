# Changelog

Alla noterbara ändringar i detta projekt dokumenteras i den här filen.  
Formatet är baserat på [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
och detta projekt följer [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

- Stöd för fler System Nexa 2-enheter
- Power consumption / energimätning (om API stöder det)
---

## [0.3.0] – 2025-09-16
### Added
- Full WebSocket support (control + state updates)
- Automatic login handshake
- Fallback to HTTP if WS fails
- Tools: added `test_ws.py` for manual WS testing


---
## [0.2.0] – 2025-09-16
### Added
- Configurable **port** field in the Config Flow (defaults to 3000).
- Host can be specified as `host:port`; if so, Port field is ignored.

---

## [0.1.0] – 2025-09-16
### Added
- Första release av **System Nexa 2 (DIY)** för Home Assistant
- Stöd för **WPD-01** som *light entity* med brightness (0–255)
- Lokalt HTTP-API (`/state`, `/state?on=0|1`, `/state?v=0.0–1.0`)
- Config Flow (IP, token, namn, poll interval)
- HACS-stöd via `hacs.json`
- README + dokumentation i `docs/`

---

[Unreleased]: https://github.com/YOURNAME/homeassistant-systemnexa2/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/YOURNAME/homeassistant-systemnexa2/releases/tag/v0.1.0
