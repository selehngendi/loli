# Molty Royale AI Agent Fleet v3.0

Jalankan hingga **10 agent sekaligus** dalam 1 Railway service menggunakan Python asyncio.

## 🚀 Deploy ke Railway

### Variabel Wajib
| Variable | Deskripsi |
|----------|-----------|
| `AGENT_COUNT` | Jumlah agent yang berjalan (1–10, default: 1) |
| `RAILWAY_API_TOKEN` | Token Railway untuk auto-sync credentials |

### Variabel Per Agent
Untuk setiap agent `i` (1 s/d `AGENT_COUNT`), isi variabel berikut.  
**Kosongkan semua** → bot auto-generate wallet baru saat pertama jalan.  
**Isi dari akun lama** → bot pakai wallet yang sama.

| Variable | Keterangan |
|----------|-----------|
| `AGENT_{i}_NAME` | Nama agent (default: `MoltyAgent{i}`) |
| `AGENT_{i}_API_KEY` | API key (auto-generated jika kosong) |
| `AGENT_{i}_PRIVATE_KEY` | Agent private key (auto-generated) |
| `AGENT_{i}_WALLET_ADDRESS` | Agent wallet address (auto-generated) |
| `AGENT_{i}_OWNER_EOA` | Owner wallet address (auto-generated) |
| `AGENT_{i}_OWNER_KEY` | Owner private key (auto-generated) |

### Contoh Raw Editor (10 Agent)
Paste ke **Variables → Raw Editor**:
```
AGENT_COUNT=10
RAILWAY_API_TOKEN=
ROOM_MODE=free
LOG_LEVEL=INFO

AGENT_1_NAME=MoltyAgent1
AGENT_1_API_KEY=
AGENT_2_NAME=MoltyAgent2
AGENT_2_API_KEY=
AGENT_3_NAME=MoltyAgent3
AGENT_3_API_KEY=
AGENT_4_NAME=MoltyAgent4
AGENT_4_API_KEY=
AGENT_5_NAME=MoltyAgent5
AGENT_5_API_KEY=
AGENT_6_NAME=MoltyAgent6
AGENT_6_API_KEY=
AGENT_7_NAME=MoltyAgent7
AGENT_7_API_KEY=
AGENT_8_NAME=MoltyAgent8
AGENT_8_API_KEY=
AGENT_9_NAME=MoltyAgent9
AGENT_9_API_KEY=
AGENT_10_NAME=MoltyAgent10
AGENT_10_API_KEY=
```
Setelah deploy pertama, Railway akan otomatis mengisi `API_KEY`, `PRIVATE_KEY`, dll per agent.

---

## 💡 Cara Pindah Akun (Gunakan Wallet Lama)
Cukup isi variabel `AGENT_{i}_PRIVATE_KEY`, `AGENT_{i}_OWNER_KEY`, dan `AGENT_{i}_API_KEY`  
dari akun Railway yang lama. Bot tidak akan generate wallet baru.

## 🏗️ Arsitektur
```
main.py
  └── asyncio.gather(
        AgentRunner(1),  ← wallet di dev-agent-1/
        AgentRunner(2),  ← wallet di dev-agent-2/
        ...
        AgentRunner(10), ← wallet di dev-agent-10/
      )
```
Setiap agent berjalan independen. Jika 1 agent error, yang lain tetap berjalan.
