# DIY Mode – System Nexa 2

System Nexa 2 devices (e.g. WPD-01) can run in **DIY mode**, which disables the Nexa Cloud and allows full **local control** over HTTP and WebSocket.

---

## 🔹 What happens in DIY mode?

| Mode        | Nexa App (LAN) | Nexa App (WAN) | Local API (HTTP/WS) | Home Assistant |
|-------------|----------------|----------------|---------------------|----------------|
| Cloud (default) | ✅ Works everywhere | ✅ Works | ❌ Not available | ❌ |
| DIY (`diy_mode=1`) | ⚠️ Works only on same Wi-Fi | ❌ Offline | ✅ Works | ✅ |

- In DIY mode, the device **stops talking to Nexa Cloud**.  
- The mobile app will **only work when your phone is on the same LAN**.  
- Remote WAN access (outside your home) is disabled.  
- Home Assistant and local API work **without the cloud**.

---

## 🔹 Enable DIY mode

1. Make sure the device is connected to Wi-Fi and has an IP (check in router or app).  
2. Send this request to enable DIY mode:

   ```bash
   curl -X POST http://<device_ip>:3000/settings \
        -H "Content-Type: application/json" \
        -d '{"diy_mode":1,"store":1}'
