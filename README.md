# 🎬 Movie Code Bot

Telegram kino bot — kodlar orqali filmlarni channel'dan yetkazib beradi.

---

## ⚡ TEZKOR ISHGA TUSHIRISH

### 1. O'rnatish
```bash
pip install -r requirements.txt
```

### 2. Sozlash — `config.py`
```python
BOT_TOKEN  = "1234567890:ABCdef..."   # @BotFather dan
ADMIN_ID   = 123456789                 # Sizning Telegram ID ingiz
CHANNEL_ID = "@mymoviechannel"         # Kino channel
```

### 3. Ishga tushirish
```bash
python bot.py
```

---

## 📁 LOYIHA STRUKTURASI

```
project/
├── bot.py              # Entry point
├── config.py           # Sozlamalar
├── db.py               # SQLite operatsiyalar
├── requirements.txt
│
├── handlers/
│   ├── admin.py        # Admin komandalar
│   ├── user.py         # User komandalar + inline buttons
│   └── channel.py      # Channel post auto-detect
│
└── services/
    ├── cache_service.py # RAM cache
    └── movie_service.py # Kino yuborish logikasi
```

---

## 🔧 CHANNELNI SOZLASH

1. Kino channel yarating
2. Botni channel'ga **admin** qiling (post ko'rish huquqi bilan)
3. `config.py` da `CHANNEL_ID` ni kiriting

### Channel post formati:
```
🎬 John Wick
#001
```
Bot avtomatik ushbu postni topib, kodni DB ga saqlaydi.

**Premium kino** uchun `P` prefixi ishlating:
```
🎬 Avengers: Endgame
#P001
```

---

## 🎮 KOMANDALAR

### 👤 Foydalanuvchi
| Komanda | Tavsif |
|---------|--------|
| `/start` | Botni ishga tushirish |
| `/help` | Yordam |
| `/search John Wick` | Kino qidirish |
| `/random` | Tasodifiy kino |
| `/mystats` | Shaxsiy statistika |
| `/referral` | Do'st taklif havolasi |

### 🔐 Admin
| Komanda | Tavsif |
|---------|--------|
| `/add 001 John Wick 12345` | Kino qo'shish |
| `/delete 001` | Kino o'chirish |
| `/edit 001 John Wick 2` | Nomini o'zgartirish |
| `/stats` | Bot statistikasi |
| `/setpremium 123456789` | Premium berish |

---

## 💎 PREMIUM TIZIMI

- **Free** kinolar: barcha foydalanuvchilar
- **Premium** kinolar (P prefixi): faqat premium users
- Premium olish: 5 do'st taklif qilish yoki admin orqali

---

## ⚡ CACHE TIZIMI

- Bot ishga tushganda DB dagi barcha kinolar RAM ga yuklanadi
- Yangi kino qo'shilganda cache ham yangilanadi
- Restart bo'lganda DB dan qayta yuklanadi

---

## 🔑 ADMIN_ID OLISH

1. Telegram da `@userinfobot` ga yozing
2. U sizning ID ingizni beradi
3. Shu raqamni `config.py` ga kiriting

---

## 🌐 SERVER DA ISHLATISH (Production)

```bash
# systemd service yaratish
sudo nano /etc/systemd/system/moviebot.service
```

```ini
[Unit]
Description=Movie Code Bot
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/movie_bot
Environment="BOT_TOKEN=YOUR_TOKEN"
Environment="ADMIN_ID=123456789"
Environment="CHANNEL_ID=@yourchannel"
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable moviebot
sudo systemctl start moviebot
sudo systemctl status moviebot
```
