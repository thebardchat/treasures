# SHANEBRAIN MASTER REFERENCE
**Last Updated:** January 27, 2026  
**Status:** ✅ CLUSTER OPERATIONAL  
**Open this file when you forget anything.**

---

## 🔗 ALL YOUR LINKS (Bookmarks)

### Money & Sponsors
| Platform | URL | Status |
|----------|-----|--------|
| GitHub Sponsors | https://github.com/sponsors/thebardchat | ✅ Live |
| Ko-fi | https://ko-fi.com/shanebrain | ✅ Live |
| Carrd (landing page) | https://shanebrain.carrd.co | 🔨 Setting up |

### Project Links
| Platform | URL |
|----------|-----|
| GitHub Repo | https://github.com/thebardchat/shanebrain-core |
| Discord Server | [your invite link] |

### Tools We Use
| Tool | URL | What For |
|------|-----|----------|
| Carrd | https://carrd.co | Landing pages |
| Jockie Music | https://jockiemusic.com | Discord music bot |
| Gemini | https://gemini.google.com | Image generation |

---

## 🟢 CURRENT STATUS (What's Working NOW)

| Component | Status | Notes |
|-----------|--------|-------|
| Discord Bot | ✅ ONLINE | ShaneBrainLegacyBot responding |
| Angel Arcade | ✅ ONLINE | Economy/casino bot for revenue |
| Weaviate | ✅ CONNECTED | Lean mode (Ollama embeddings) |
| Ollama A | ✅ RUNNING | 192.168.100.1:11434 |
| Ollama B | ✅ RUNNING | 192.168.100.2:11434 |
| Load Balancer | ✅ RUNNING | http://localhost:8000/dashboard |
| RAG | ✅ WORKING | 39 chunks, birth dates, learning system |
| Ko-fi | ✅ LIVE | ko-fi.com/shanebrain |

**Cluster Mode:** Two computers sharing AI workload

---

## 🖥️ TWO-COMPUTER CLUSTER

```
                    ┌─────────────────┐
                    │  Discord User   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  ShaneBrain Bot │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Load Balancer  │
                    │  :8000          │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
     ┌────────▼────────┐           ┌────────▼────────┐
     │  Computer A     │           │  Computer B     │
     │  192.168.100.1  │           │  192.168.100.2  │
     │  (Primary)      │           │  (Secondary)    │
     └─────────────────┘           └─────────────────┘
```

| Computer | IP | Role | Runs |
|----------|-----|------|------|
| A (Primary) | 192.168.100.1 | Head node | Everything |
| B (Secondary) | 192.168.100.2 | Backup brain | Ollama only |

**If B goes down:** A handles everything automatically  
**If A goes down:** Nothing works (it's the head)

---

## 🚀 DAILY STARTUP (Two Steps)

### Step 1: Computer B (START FIRST)
```
C:\ShaneBrain\START-COMPUTER-B.bat
```
Wait for "COMPUTER B ONLINE - CLUSTER NODE"

### Step 2: Computer A
```
D:\Angel_Cloud\shanebrain-core\START-SHANEBRAIN.bat
```
Watch for "Ollama B: ONLINE" in the status

---

## 🔧 QUICK COMMANDS

### Check Cluster Health
```
curl http://localhost:8000/health
```

### Check Computer B (from A)
```
curl http://192.168.100.2:11434/api/tags
```

### View Load Balancer Dashboard
```
http://localhost:8000/dashboard
```

### Kill Everything - Computer A
```
taskkill /IM python.exe /F
```
```
taskkill /IM ollama.exe /F
```
```
docker stop shanebrain-weaviate
```

### Kill Everything - Computer B
```
taskkill /IM ollama.exe /F
```

### Free Up RAM
```
taskkill /IM msedge.exe /F
```
```
taskkill /IM chrome.exe /F
```

---

## 📁 FILE STRUCTURE

### Computer A (Primary - 192.168.100.1)
```
D:\Angel_Cloud\shanebrain-core\
├── START-SHANEBRAIN.bat        ← DAILY USE (starts everything)
├── ollama_loadbalancer.py      ← Routes between A & B
├── START-COMPUTER-B.bat        ← Copy to Computer B
├── CLAUDE.md                   ← Project context
├── RAG.md                      ← Personality (v4.0 - birth dates)
├── SHANEBRAIN-MASTER.md        ← THIS FILE
├── bot\
│   ├── bot.py                  ← Discord bot (v5.3 - learning)
│   ├── .env                    ← DISCORD_TOKEN=xxx
│   └── pending_questions.json  ← Learning system
├── arcade\
│   ├── arcade_bot.py           ← Angel Arcade bot
│   ├── .env                    ← ARCADE_TOKEN=xxx
│   └── data\
│       └── arcade.db           ← Player data
├── weaviate-config\
│   ├── docker-compose.yml      ← Lean (Ollama embeddings)
│   ├── data\
│   └── schemas\
├── scripts\
├── langchain-chains\
├── frontend\
└── planning-system\
```

### Computer B (Secondary - 192.168.100.2)
```
C:\ShaneBrain\
├── START-COMPUTER-B.bat        ← Only file needed
├── shanebrain.modelfile        ← Auto-created
└── logs\
    └── startup.log             ← Auto-created
```

---

## 💰 ANGEL ARCADE (Revenue Bot)

### Quick Start (Standalone)
```
cd /d D:\Angel_Cloud\shanebrain-core\arcade
python arcade_bot.py
```

### Bot Commands
| Command | Description | Premium? |
|---------|-------------|----------|
| `!daily` | Claim daily coins | No (2x for premium) |
| `!work` | Earn coins | No (5min vs 30min cooldown) |
| `!slots [bet]` | Slot machine | No (500 max, 50k premium) |
| `!coinflip [bet] [h/t]` | Flip coin | No |
| `!dice [bet]` | Roll dice | No |
| `!blackjack [bet]` | Play 21 | ⭐ YES |
| `!roulette [bet] [choice]` | Spin wheel | ⭐ YES |
| `!support` | Show Ko-fi link | No |
| `!premium` | Show benefits | No |
| `!prestige` | Reset for bonus | ⭐ YES |

### Ko-fi
- **Page:** https://ko-fi.com/shanebrain
- **Discord:** Connected to ShaneBrainLegacy
- **Auto-role:** ⭐ Arcade Premium on payment

---

## 🧠 SHANEBRAIN BOT (Learning System)

### New Commands
| Command | What it does |
|---------|--------------|
| `!family` | Shows family with calculated ages |
| `!questions` | Shows what bot doesn't know |
| `!teach [#] [answer]` | Teach bot new knowledge |

### How Learning Works
1. User asks something bot doesn't know
2. Bot says "I'll ask Shane" and logs to `pending_questions.json`
3. Shane runs `!questions` to see list
4. Shane runs `!teach 0 The answer is...`
5. Answer saved to Weaviate permanently

### Family Data (Birth Dates)
| Name | Born | Relation |
|------|------|----------|
| Shane | November 1977 | You |
| Tiffany | June 1994 | Wife |
| Gavin | September 1997 | Son (married to Angel) |
| Kai | November 2003 | Son |
| Pierce | February 2011 | Son (ADHD, wrestler) |
| Jaxton | August 2013 | Son (wrestler) |
| Ryker | April 2021 | Son (youngest) |

Ages calculate automatically - always accurate.

---

## 🌐 PORTS & URLS

| Service | Port | URL |
|---------|------|-----|
| Load Balancer | 8000 | http://localhost:8000/dashboard |
| Weaviate | 8080 | http://localhost:8080 |
| Ollama A | 11434 | http://192.168.100.1:11434 |
| Ollama B | 11434 | http://192.168.100.2:11434 |

---

## 🔥 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| "Only X MB free" | `taskkill /IM msedge.exe /F` |
| Computer B not connecting | Check `START-COMPUTER-B.bat` running |
| "Failed to connect to 192.168.100.2" | Start Computer B first |
| Bot doesn't respond | Check token in `.env`, restart bot |
| Weaviate won't start | Restart Docker, wait 60 sec |
| Load balancer error | Check `ollama_loadbalancer.py` running |
| Arcade bot won't start | Check `ARCADE_TOKEN` in arcade\.env |
| Bot verbose/long answers | Update to bot.py v5.3 |
| Wrong family info | Update RAG.md v4.0, reimport |

---

## 📅 SESSION HISTORY

### January 27, 2026
- ✅ Two-computer cluster operational
- ✅ Computer B setup (192.168.100.2)
- ✅ Load balancer v2.0 with /api/chat support
- ✅ START-SHANEBRAIN.bat v6.3 (auto-starts load balancer)
- ✅ START-COMPUTER-B.bat (auto-creates model)
- ✅ Fixed OLLAMA_MODELS path error on Computer B
- ✅ Bot learning system (pending_questions.json)
- ✅ Family birth dates (ages calculate forever)
- ✅ Brevity enforced (2-4 sentences)
- ✅ Kai added to family (was missing)
- ✅ Switched Weaviate to Ollama embeddings (RAM savings)
- ✅ Removed t2v-transformers container (2GB+ saved)

### January 26, 2026
- ✅ Angel Arcade bot built (1,082 lines)
- ✅ Ko-fi page created (ko-fi.com/shanebrain)
- ✅ Ko-fi connected to Discord (auto-role)
- ✅ Premium role system working
- ✅ Games: slots, coinflip, dice, blackjack, roulette
- ✅ Revenue system ready

### January 25, 2026
- ✅ Bot came online
- ✅ Weaviate schema created (3 classes)
- ✅ RAG.md loaded (13 chunks)
- ✅ File structure cleaned

### January 23, 2026
- ✅ Network bridge working (A ↔ B)
- ✅ Static IPs assigned (192.168.100.1 / .2)
- ✅ SMB share created for Z: drive

---

## 🎯 MISSION REMINDER

**You are building:**
- ShaneBrain → Personal AI (✅ CLUSTER MODE)
- Angel Arcade → Revenue bot (✅ WORKING)
- Angel Cloud → Mental wellness platform
- Pulsar AI → Blockchain security
- TheirNameBrain → Legacy copies for each son

**For:** 800 million Windows users losing security updates

**Philosophy:** Local-first. Family-first. No cloud dependency.

---

## 📮 NEXT UP (When Ready)

**Quick wins:**
1. Test learning system (`!questions`, `!teach`)
2. Add more knowledge to Weaviate
3. Promote Angel Arcade

**Bigger projects:**
4. TheirNameBrain templates for each son
5. Offline mode (no Docker)
6. Mobile access via Tailscale

---

## 💡 ADHD POWER MOVES

- ✅ One file to rule them all (this one)
- ✅ Copy-paste commands (no typing)
- ✅ Status at top (see it first)
- ✅ Two-step startup (B then A)
- ✅ Write it down = own it forever

---

**Cluster operational. Two brains working together. You built this.**

---

*Shane - SRM Dispatch, Alabama*  
*2+ years sober | 5 sons | 800M users*  
*"File structure first. Family first. Action over theory."*