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
   ```sh
   pip install -r requirements.txt
   ```
3. **Hozz létre egy `config.ini` fájlt az `config.example.ini` alapján**.
4. **Indítsd el a szervert**:
   ```sh
   python main.py
   ```

---

## 🔧 Konfiguráció (`config.ini`)
A `config.ini` fájlban állíthatók be a szerver alapvető funkciói.

```ini
[settings]
ENABLE_COMMANDS = True    # Parancsok engedélyezése
SSL_ENABLED = False       # SSL titkosítás bekapcsolása
SERVER_PORT = 8000        # Szerver port
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
| `requirements.txt` | A függőségek listája |

---

## 🚀 Fejlesztés & Jövőbeli tervek
- [ ] **További parancsok bővítése**
- [ ] **Biztonsági fejlesztések (pl. autentikáció)**
- [ ] **Kliens verzió fejlesztése & verziókezelés**

---

## 📅 Licenc & Hozzájárulás
*(Ide jöhet egy licenc infó, pl. MIT License, ha szeretnéd nyilvánosan megosztani.)*

---

Ez egy alap README, amit **tetszőlegesen bővíthetsz**. 😊 Mit gondolsz, megfelel így az alapstruktúra?
