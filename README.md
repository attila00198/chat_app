# WebSocket Chat Server

Ez egy egyszerű WebSocket alapú chat szerver, amely támogatja a felhasználói listákat, parancsokat, valamint az SSL opciót.

---

## ⚡ Telepítés

1. **Klónozd a repót**:
   ```sh
   git clone https://github.com/felhasznalonev/chat-server.git
   cd chat-server
   ```
2. **Telepítsd a függőségeket**:
   2.a ***Windows rendszeren***:
   ```sh
   pip install -r requirements.txt
   ```
   2.b. ***Debian/ubuntu rendszeren***:
   ```sh
   python -m venv venv
   source ./venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Hozz létre egy `config.ini` fájlt az `config.example.ini` alapján**.
5. **Indítsd el a szervert**:
   ```sh
   python main.py
   ```

---

## 🔧 Konfiguráció (`config.ini`)
A `config.ini` fájlban állíthatók be a szerver alapvető funkciói.

```ini
# To setup your websocket chat server rename of copy this file as config.ini

# Websocket server host/port
[server]
host = localhost
port = 8000

# If you want to use SSL suport set up this section - default fale
[ssl]
use_ssl = false
ssl_certfile = /path/to/cert.pem
ssl_keyfile = /path/to/privkey.pem

# Enable/disable commands - default true
[commands]
# This setting is not working a this time
enable_commands = true

```

---

## 🔗 WebSocket Működés
A szerver a következő eseményeket kezeli:

### ⭐ Chat Üzenet küldése
**Bejövő (kliens -> szerver):**
```json
{
  "type": "message",
  "sender": "User123",
  "content": "Hello!"
}
```

**Kimenő (szerver -> kliens):**
```json
{
  "type": "message",
  "sender": "User123",
  "content": "Hello!"
}
```

### 📆 Felhasználólista frissítése
A szerver esemény alapon **automatikusan elküldi a frissített listát**, ha valaki belép vagy kilép.

**Kimenő (szerver -> kliens):**
```json
{
  "type": "user_list_update",
  "sender": "System",
  "content": ["User1", "User2", "User3"]
}
```

---

## 🛠️ Parancsok
A chat szerver **`/` prefixszel ellátott parancsokat** is kezel, ha engedélyezve van.

### ⭐ Elérhető parancsok
| Parancs | Funkció |
|---------|---------|
| `/listUsers` | Listázza az összes jelenlegi felhasználót |

További parancsok a jövőben lesznek bővítve!

---

## 📁 Fájlstruktúra

| Fájl | Funkció |
|-------|---------|
| `main.py` | A szerver belépési pontja |
| `ws_server.py` | WebSocket kezelés (neve változhat) |
| `client_manager.py` | A kliensek kezelése |
| `command_manager.py` | Parancsok feldolgozása |
| `command_list.py` | Előre definiált parancsok |
| `logging_config.py` | Logging konfiguráció |
| `requirements.txt` | A függőségek listája |

---

## 🚀 Fejlesztés & Jövőbeli tervek
- [ ] **További parancsok bővítése**
- [ ] **Biztonsági fejlesztések (pl. autentikáció)**
- [ ] **Emoji használat integráció (pl. :smile:)**
- [ ] **Kliens verzió fejlesztése & verziókezelés**

---

## 📅 Licenc & Hozzájárulás
*MIT*

