# Molty Royale AI Agent Bot v2.0

Autonomous AI agent for [Molty Royale](https://www.moltyroyale.com/) battle royale game.

## 🚀 One-Click Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/selehngendi/lola&envs=AGENT_NAME,RAILWAY_API_TOKEN,ROOM_MODE,LOG_LEVEL,ADVANCED_MODE,AUTO_WHITELIST,AUTO_SC_WALLET,ENABLE_MEMORY,ENABLE_AGENT_TOKEN,AUTO_IDENTITY&optionalEnvs=ROOM_MODE,LOG_LEVEL,ADVANCED_MODE,AUTO_WHITELIST,AUTO_SC_WALLET,ENABLE_MEMORY,ENABLE_AGENT_TOKEN,AUTO_IDENTITY&ROOM_MODE=free&LOG_LEVEL=INFO&ADVANCED_MODE=true&AUTO_WHITELIST=true&AUTO_SC_WALLET=true&ENABLE_MEMORY=true&ENABLE_AGENT_TOKEN=false&AUTO_IDENTITY=true)

Klik tombol di atas, lalu isi **2 variabel wajib**:
- `AGENT_NAME` — Nama bot agent kamu
- `RAILWAY_API_TOKEN` — Buat di: https://railway.com/account/tokens

Variabel lainnya sudah terisi default. Bot akan auto-generate API_KEY, wallet, dan credentials lainnya saat pertama kali jalan.

---

## ⚙️ Environment Variables

### Wajib Diisi
| Variable | Deskripsi |
|----------|-----------|
| `AGENT_NAME` | Nama bot agent (max 50 chars) |
| `RAILWAY_API_TOKEN` | Token untuk auto-sync credentials. Buat di [railway.com/account/tokens](https://railway.com/account/tokens) |

### Default (sudah terisi otomatis)
| Variable | Default | Deskripsi |
|----------|---------|-----------|
| `ROOM_MODE` | `free` | `free` / `auto` / `paid` |
| `LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` |
| `ADVANCED_MODE` | `true` | Auto-generate Owner+Agent wallet |
| `AUTO_WHITELIST` | `true` | Auto whitelist approval |
| `AUTO_SC_WALLET` | `true` | Auto-create SC Wallet |
| `ENABLE_MEMORY` | `true` | Cross-game learning |
| `ENABLE_AGENT_TOKEN` | `false` | Agent token registration |
| `AUTO_IDENTITY` | `true` | Auto ERC-8004 identity |

### Strategy Tuning (opsional)
| Variable | Default | Deskripsi |
|----------|---------|-----------|
| `AGGRESSION_LEVEL` | `balanced` | `passive` / `balanced` / `aggressive` |
| `HP_CRITICAL` | `25` | HP threshold healing darurat |
| `HP_MODERATE` | `60` | HP threshold healing normal |
| `GUARDIAN_FARM_HP` | `30` | Min HP untuk farm guardian |
| `COMBAT_MIN_EP` | `2` | Min EP untuk combat |

### Auto-Generated (jangan diisi manual)
Bot akan mengisi variabel berikut secara otomatis saat first-run:
- `API_KEY` — Dari POST /accounts
- `AGENT_WALLET_ADDRESS` — Generated Agent EOA
- `AGENT_PRIVATE_KEY` — Generated Agent private key
- `OWNER_EOA` — Generated Owner EOA
- `OWNER_PRIVATE_KEY` — Generated Owner private key

---

## 🏗️ Manual Deploy

```bash
# Clone
git clone https://github.com/selehngendi/lola.git
cd lola

# Install
pip install -r requirements.txt

# Copy env
cp .env.example .env
# Edit .env — isi AGENT_NAME dan RAILWAY_API_TOKEN

# Run
python -m bot.main
```

## 📊 Dashboard
Bot menyertakan web dashboard untuk monitoring real-time di `http://localhost:8080`.

## 📋 Raw Editor (untuk service yang sudah ada)
Jika service sudah dibuat, paste ini ke **Variables → Raw Editor**:
```
AGENT_NAME=
ROOM_MODE=free
LOG_LEVEL=INFO
ADVANCED_MODE=true
AUTO_WHITELIST=true
AUTO_SC_WALLET=true
ENABLE_MEMORY=true
ENABLE_AGENT_TOKEN=false
AUTO_IDENTITY=true
RAILWAY_API_TOKEN=
```
Lalu isi `AGENT_NAME` dan `RAILWAY_API_TOKEN`.
