<div align="center">

<img width="100%" alt="header" src="https://capsule-render.vercel.app/api?type=waving&height=210&text=Wieners%20Farm%20Bot&fontAlign=50&fontAlignY=36&fontSize=56&desc=Farm%20%7C%20Daily%20Check-in%20%7C%20Spin%20%7C%20Ads%20%7C%20Withdrawal%20Unlock&descAlign=50&descAlignY=58"/>

<img alt="typing" src="https://readme-typing-svg.demolab.com?font=Inter&size=18&duration=3000&pause=650&center=true&vCenter=true&width=900&lines=Auto+Farm+%7C+Claim+All+Daily+Cycles;Auto+Daily+Check-in+%7C+Earn+WIENER+Reward;Auto+Spin+%7C+Earn+Ad+Credits+%26+Spin+All;Auto+Watch+Ads+%7C+Full+Daily+Quota+Covered;Auto+Withdrawal+Unlock+%7C+Watch+Required+Ads"/>

<p>
  <img alt="python" src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white"/>
  <img alt="platform" src="https://img.shields.io/badge/Platform-Wieners%20Farm%20Miniapp-111111"/>
  <img alt="multi-account" src="https://img.shields.io/badge/Multi--Account-Supported-111111"/>
  <img alt="proxy" src="https://img.shields.io/badge/Proxy-Supported-111111"/>
  <img alt="author" src="https://img.shields.io/badge/by-Yuurisandesu-111111"/>
</p>

<p>
  <b>Wieners Farm Bot</b> is a full automation bot for the Wieners Farm Telegram Miniapp.<br/>
  It handles the complete daily cycle: registering a persistent device fingerprint, starting the farm, claiming the daily check-in reward, earning ad spin credits and spinning all free and credit spins, claiming all available daily farm rewards, watching all available earn ads until the daily cap, and watching the required withdrawal unlock ads to enable withdrawals, all running automatically across multiple accounts with proxy support and a live countdown between cycles.<br/>
  Built and distributed by <b>Yuurisandesu</b>.
</p>

</div>

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Features](#features)
- [File Structure](#file-structure)
- [Disclaimer](#disclaimer)

---

## Requirements

- Python `3.12+`
- Git

---

## Installation

**Clone the repository:**

```bash
git clone https://github.com/Yuurisan-N1/Wienerfarm-Miniapp.git
cd Wienerfarm-Miniapp
```

**Install dependencies:**

```bash
pip install requests yuurisan
```

---

## Configuration

### 1. Accounts (data.txt)

Fill `data.txt` with Telegram WebApp `initData` for each account, one per line:

```
user=%7B%22id%22...&hash=abc123
user=%7B%22id%22...&hash=def456
```

> `initData` can be obtained from the browser DevTools when opening Wieners Farm on Telegram Web.

### 2. Proxy (proxy.txt)

Fill `proxy.txt` with proxies, one per line (optional, leave empty to run without proxy):

```
host:port
host:port:user:pass
http://user:pass@host:port
```

Proxies are assigned to accounts by index in round-robin order.

### 3. Bot Settings (config.json)

`sleep_seconds` controls how many seconds the bot waits between cycles.

---

## Running the Bot

```bash
python bot.py
```

Press `Ctrl+C` at any time to stop the bot cleanly.

---

## Features

### Device Fingerprint Registration
Each account gets a unique set of device identifiers: a device ID, installation ID, device fingerprint, and fingerprint v2, all generated once and saved to `device.json`. On subsequent runs, the same identifiers are reused for each account so the device stays consistent across cycles.

### Auto Farm
The bot checks the current farm session state. If no session is active, it starts one. It then claims all remaining farm reward slots for the day based on the daily limit and how many have already been claimed. Each successful claim is logged.

### Daily Check-in
The bot checks whether the daily check-in has been claimed today. If not, it claims it and logs the day number and WIENER reward. If already done, it is skipped silently.

### Auto Spin
The bot fetches the spin status and earns all remaining ad spin credits first. Each credit requires starting an ad session, waiting 15 seconds, then claiming the credit with server-issued session ID. If the server returns a cooldown after a credit, the bot waits it out automatically. After all credits are earned, the bot spins all free spins and ad credit spins in sequence. Each spin logs the reward type and amount. A random delay of 1.5 to 3 seconds is applied between spins.

### Auto Ads
The bot fetches the daily ad status and checks how many slots remain under the daily cap. It then watches ads in a loop until the cap is reached. Each ad requires starting a session, waiting 15 seconds, then completing it with the session ID. Any cooldown returned by the server is respected before the next ad. Each completed ad logs the WIENER reward and remaining slots.

### Withdrawal Unlock Ads
The bot checks whether the withdrawal feature has been unlocked for the account. If not, it watches the required number of ads to unlock it. Each ad requires starting a session, waiting 15 seconds, then crediting it. Progress toward the required count is logged after each credit. A random delay of 2 to 4 seconds is applied between withdrawal ads.

### Random Device Headers
Every request uses a randomly generated User-Agent combining a random Android version (10 to 16), a random Chrome version (118 to 153), a random Telegram app version, and a random device model from a pool of 8 devices. The `x-requested-with` header is also randomized from a pool of 8 Telegram client packages.

### Multi Account
All accounts in `data.txt` are processed sequentially within every cycle. Username, balance, and streak are logged at the start of each account. The cycle number is logged after all accounts complete.

### Proxy Support
Proxies are loaded from `proxy.txt` and assigned to accounts by position in round-robin order. Proxy credentials are masked in log output. Running without proxies is fully supported.

### Auto Countdown
After all accounts complete a cycle, the bot displays a live `HH:MM:SS` countdown until the next cycle starts.

---

## File Structure

```text
Wienerfarm-Miniapp/
├── bot.py          # Main bot, full daily cycle automation
├── config.json     # Sleep duration between cycles
├── data.txt        # Account initData, one per line
├── proxy.txt       # Proxy list, one per line (optional)
├── device.json     # Per-account device fingerprint cache (auto-generated)
├── LICENSE         # License file
└── utils/
    └── banner.py   # Banner display on startup
```

---

## Disclaimer

This tool is built for educational and technical exploration purposes. Use it wisely and at your own responsibility.

---

<div align="center">
<img width="100%" alt="footer" src="https://capsule-render.vercel.app/api?type=waving&height=120&section=footer"/>
</div>