# Changelog

Alla noterbara ändringar i detta projekt dokumenteras i den här filen.  
Formatet följer [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
och versionering följer [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]
- Power consumption / energimätning (om API stöder det)

---
## [1.0.1] – 2025-09-17
### Added
- Deterministiska unique_id för config entries och entiteter
- Stabil device identifier per fysisk enhet (host:port)
- Validering i config flow → samma host:port kan inte läggas till två gånger

### Notes
- Befintliga entiteter utan unique_id behöver läggas in på nytt

---

## [1.0.0] – 2025-09-XX
### Added
- Första officiella release 🎉
- Fullt stöd för WPD-01, WBD-01 (dimmer) samt WPR-01, WPO-01, WBR-01 (switch)
- WebSocket + HTTP fallback för styrning och status
- Dimning med 2-decimals avrundning (0–100 %)
- Config Flow (GUI) med modellval
- DeviceInfo med korrekt modell + config URL
- Migration inbyggd (gamla entries uppdateras automatiskt)

---

## [0.4.0] – 2025-09-16 (Pre-release)
### Added
- Stöd för flera Nexa-modeller:
  - **WPD-01**, **WBD-01** (dimmer → light)
  - **WPR-01**, **WPO-01**, **WBR-01** (på/av → switch)
- Modelldropdown i Config Flow
- DeviceInfo med korrekt modell + config-URL
- Migration (`async_migrate_entry`) så gamla entries överlever uppgraderingar

### Changed
- Gemensam koordinator används för alla modeller
- Samma WS + HTTP fallback för styrning och status
- Post-send refresh efter kommandon för bättre synk

---
## [0.3.5] – 2025-09-16
### Added
- Stöd för HTTP-svar i format `{"state": <float>}`
- Post-send refresh efter varje skickat värde för säkrare synk

### Changed
- Kommandon skickas som numeriska värden över WS
- Dimnivåer avrundas konsekvent till 2 decimaler

---

## [0.3.3] – 2025-09-16
### Added
- Persistent WebSocket för status **och** kommandon
- Automatisk login-handshake vid WS-anslutning
- HTTP fallback om WS-sändning misslyckas
- Dimnivåer avrundas till 2 decimaler innan de skickas
- Kommandon skickas nu via samma WS-session som status
- HTTP fallback om WS skick misslyckas

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
