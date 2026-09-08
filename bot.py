import os
import sys
import json
import time
import uuid
import random
import hashlib
import signal
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils.banner import show_banner

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"

MY_PROJECT = "Wieners Farm Miniapp"

def log_green(msg):
    print(f"{GREEN}{BOLD}{msg}{RESET}")

def log_yellow(msg):
    print(f"{YELLOW}{BOLD}{msg}{RESET}")

def log_red(msg):
    print(f"{RED}{BOLD}{msg}{RESET}")

def signal_handler(sig, frame):
    print()
    log_red("Script stopped by user.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

ANDROID_VERSIONS = ["10", "11", "12", "13", "14", "15", "16"]
CHROME_VERSIONS = ["118", "120", "122", "124", "126", "128", "130", "132", "134", "136", "138", "140", "142", "144", "146", "148", "150", "151", "152", "153"]
TG_VERSIONS = ["10.9.1", "11.0.0", "11.1.0", "11.2.1", "11.3.0", "11.5.2", "12.0.0", "12.1.0", "12.3.1", "12.5.0", "12.7.0", "12.9.2"]
DEVICES = ["Oppo CPH2631", "Samsung SM-G991B", "Xiaomi 2201123G", "Redmi Note 11", "Vivo V2109", "Realme RMX3430", "OnePlus LE2101", "Poco X4 Pro"]
X_REQUESTED_WITH_LIST = [
    "uz.unnarsx.cherrygram",
    "org.telegram.messenger",
    "org.telegram.plus",
    "com.hanista.mobogram",
    "org.thunderdog.challegram",
    "com.nekogramx.nekogram",
    "it.owlgram.android",
    "com.exteragram.messenger",
]

def random_headers():
    android = random.choice(ANDROID_VERSIONS)
    chrome_ver = random.choice(CHROME_VERSIONS)
    tg_ver = random.choice(TG_VERSIONS)
    device = random.choice(DEVICES)
    sdk = str(random.randint(29, 36))
    xrw = random.choice(X_REQUESTED_WITH_LIST)
    ua = (
        f"Mozilla/5.0 (Linux; Android {android}; K) "
        f"AppleWebKit/537.36 (KHTML, like Gecko) "
        f"Chrome/{chrome_ver}.0.0.0 Mobile Safari/537.36 "
        f"Telegram-Android/{tg_ver} ({device}; Android {android}; SDK {sdk}; HIGH)"
    )
    return {
        "accept": "*/*",
        "accept-language": "en,en-ID;q=0.9,ja-JP;q=0.8,ja;q=0.7,id-ID;q=0.6,id;q=0.5,en-US;q=0.4",
        "apikey": "vps",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://wiener-farm.vercel.app",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://wiener-farm.vercel.app/?tgWebAppStartParam=ref_6004380466",
        "sec-ch-ua": f'"Android WebView";v="{chrome_ver}", "Not_A Brand";v="8", "Chromium";v="{chrome_ver}"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": ua,
        "x-requested-with": xrw,
    }

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def load_initdata():
    with open("data.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def load_proxies():
    if not os.path.exists("proxy.txt"):
        return []
    with open("proxy.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def get_proxy_for_index(proxies, idx):
    if not proxies:
        return None
    return proxies[idx % len(proxies)]

def mask_proxy_ip(proxy_str):
    try:
        at_idx = proxy_str.rfind("@")
        if at_idx == -1:
            return "http://user:pass@IP:port"
        host_port = proxy_str[at_idx + 1:]
        host = host_port.split(":")[0]
        port = host_port.split(":")[1] if ":" in host_port else "port"
        masked_ip = host[:2] + "*****" + host[-2:] if len(host) >= 4 else "****"
        return f"http://user:pass@{masked_ip}:{port}"
    except Exception:
        return "http://user:pass@IP:port"

def build_session(proxy_str):
    s = requests.Session()
    if proxy_str:
        s.proxies = {"http": proxy_str, "https": proxy_str}
    return s

def load_device_cache():
    if not os.path.exists("device.json"):
        return {}
    with open("device.json", "r") as f:
        content = f.read().strip()
        if not content:
            return {}
        return json.loads(content)

def save_device_cache(cache):
    with open("device.json", "w") as f:
        json.dump(cache, f, indent=2)

def get_device_data(telegram_id, cache):
    if telegram_id in cache:
        return cache[telegram_id]
    data = {
        "device_id": str(uuid.uuid4()),
        "installation_id": str(uuid.uuid4()),
        "device_fingerprint": hashlib.sha256(uuid.uuid4().bytes).hexdigest(),
        "fingerprint_v2": hashlib.sha256(uuid.uuid4().bytes).hexdigest(),
    }
    cache[telegram_id] = data
    save_device_cache(cache)
    return data

def countdown(seconds, label="Resuming in"):
    for remaining in range(int(seconds), 0, -1):
        h = remaining // 3600
        m = (remaining % 3600) // 60
        s = remaining % 60
        print(f"\r{YELLOW}{BOLD}{label} {h:02d}:{m:02d}:{s:02d}{RESET}", end="", flush=True)
        time.sleep(1)
    print("\r" + " " * 60 + "\r", end="", flush=True)

BASE = "https://wiener-farm.vercel.app/functions/v1"

def post(session, url, headers, payload):
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    r = session.post(url, headers=headers, json=payload, timeout=60, verify=False)
    r.content
    return r.json()

def api_bootstrap(session, init_data, h):
    return post(session, f"{BASE}/wiener-api", h, {"action": "bootstrap", "initData": init_data})

def api_register_device(session, init_data, device, h):
    return post(session, f"{BASE}/wiener-device", h, {
        "initData": init_data,
        "device_id": device["device_id"],
        "installation_id": device["installation_id"],
        "device_fingerprint": device["device_fingerprint"],
        "fingerprint_v2": device["fingerprint_v2"],
        "telegram_platform": "android",
        "language": "en-US",
        "timezone": "Asia/Jakarta",
    })

def api_farm_start(session, init_data, h):
    return post(session, f"{BASE}/wiener-api", h, {"action": "farm_start", "initData": init_data})

def api_farm_claim(session, init_data, h):
    return post(session, f"{BASE}/wiener-api", h, {"action": "farm_claim", "initData": init_data})

def api_daily_bio_check(session, init_data, h):
    return post(session, f"{BASE}/wiener-api", h, {"action": "daily_bio_check", "initData": init_data})

def api_daily_claim(session, init_data, h):
    return post(session, f"{BASE}/wiener-api", h, {"action": "daily_claim", "initData": init_data})

def api_spin_status(session, init_data, h):
    return post(session, f"{BASE}/wiener-spin", h, {"action": "status", "initData": init_data})

def api_spin_do(session, init_data, h):
    return post(session, f"{BASE}/wiener-spin", h, {"action": "spin", "initData": init_data, "idempotency_key": str(uuid.uuid4())})

def api_ad_spin_start(session, init_data, h):
    return post(session, f"{BASE}/wiener-spin", h, {"action": "ad_start", "initData": init_data})

def api_ad_spin_claim(session, init_data, sid, h):
    return post(session, f"{BASE}/wiener-spin", h, {"action": "ad_complete", "initData": init_data, "session_id": sid})

def api_ad_status(session, init_data, h):
    return post(session, f"{BASE}/wiener-ad-usage", h, {"action": "status", "initData": init_data})

def api_ad_start(session, init_data, h):
    return post(session, f"{BASE}/wiener-ad", h, {"action": "start", "initData": init_data})

def api_ad_complete(session, init_data, sid, h):
    return post(session, f"{BASE}/wiener-ad", h, {"action": "complete", "initData": init_data, "session_id": sid, "interacted": False})

def api_wd_status(session, init_data, h):
    return post(session, f"{BASE}/wiener-ton-wallet", h, {"action": "withdraw_ad_status", "initData": init_data})

def api_wd_ad_start(session, init_data, h):
    return post(session, f"{BASE}/wiener-ton-wallet", h, {"action": "withdraw_ad_start", "initData": init_data})

def api_wd_ad_claim(session, init_data, sid, h):
    return post(session, f"{BASE}/wiener-ton-wallet", h, {"action": "withdraw_ad_credit", "initData": init_data, "session_id": sid})

def process_account(init_data, proxy_str, device_cache):
    h = random_headers()
    session = build_session(proxy_str)

    if proxy_str:
        log_yellow(f"Connecting via proxy {mask_proxy_ip(proxy_str)}")
    else:
        log_yellow("Running without proxy for this account.")

    try:
        boot = api_bootstrap(session, init_data, h)
        if not boot.get("ok"):
            log_red("Server rejected bootstrap request, skipping account.")
            return
    except Exception as e:
        log_red(f"Bootstrap request failed: {type(e).__name__}: {e}")
        return

    user = boot["data"]["user"]
    telegram_id = user["telegram_id"]
    username = user.get("username") or user.get("first_name") or telegram_id
    balance = float(user.get("balance", 0))
    streak = user.get("daily_streak", 0)
    farm_started = user.get("farm_started_at")
    last_daily = user.get("last_daily_claim_date")
    claims_today = user.get("farm_claims_today", 0)

    device = get_device_data(telegram_id, device_cache)

    log_green(f"Account loaded for user {username}")
    log_green(f"Current balance is {balance:.2f} WIENER with a daily streak of {streak} days.")

    try:
        api_register_device(session, init_data, device, h)
        log_yellow("Device fingerprint registered with the server.")
    except Exception:
        log_yellow("Device registration encountered an issue, continuing anyway.")

    try:
        if farm_started is None:
            res = api_farm_start(session, init_data, h)
            if res.get("ok"):
                log_green("Farm session started successfully.")
            else:
                log_yellow("Farm session could not be started at this time.")
        else:
            log_yellow("Farm session is already active, skipping start.")
    except Exception:
        log_red("Failed to start farm session due to a network error.")

    try:
        from datetime import datetime, timezone
        today = datetime.now(timezone.utc).date()
        last_date = datetime.fromisoformat(last_daily.replace("Z", "+00:00")).date() if last_daily else None
        already_claimed = last_date is not None and last_date >= today
        if not already_claimed:
            bio_res = api_daily_bio_check(session, init_data, h)
            verified = bio_res.get("data", {}).get("verified", False)
            if not verified:
                log_yellow("Daily check-in not eligible, bio verification required.")
            else:
                res = api_daily_claim(session, init_data, h)
                if res.get("ok"):
                    reward = res["data"].get("reward", 0)
                    day = res["data"].get("day", 0)
                    log_green(f"Daily check-in claimed successfully for day {day} with reward {reward} WIENER.")
                else:
                    log_yellow("Daily check-in is not available at this time.")
        else:
            log_yellow("Daily check-in already completed for today, skipping.")
    except Exception:
        log_red("Failed to complete daily check-in due to a network error.")

    try:
        spin_status = api_spin_status(session, init_data, h)
        if spin_status.get("ok") and spin_status["data"].get("enabled"):
            ad_left = spin_status["data"].get("ad_left", 0)

            if ad_left > 0:
                log_yellow(f"Found {ad_left} ad spin credits to earn, processing now.")
                for _ in range(ad_left):
                    try:
                        res_start = api_ad_spin_start(session, init_data, h)
                        if not res_start.get("ok"):
                            log_red("Ad spin start request was rejected by server.")
                            break
                        sid = res_start["data"]["session_id"]
                        countdown(15, "Ad spin waiting")
                        res_claim = api_ad_spin_claim(session, init_data, sid, h)
                        if res_claim.get("ok"):
                            new_credits = res_claim["data"].get("ad_spin_credits", 0)
                            cd = res_claim["data"].get("cooldown_seconds", 0)
                            log_green(f"Ad spin credit earned, total credits now {new_credits}.")
                            if cd > 0:
                                countdown(cd, "Ad spin cooldown")
                        else:
                            log_red("Ad spin claim was rejected by server.")
                            break
                    except Exception:
                        log_red("Failed to process ad spin credit due to a network error.")
                        break

            spin_status = api_spin_status(session, init_data, h)
            free_left = spin_status["data"].get("free_left", 0)
            ad_credits = spin_status["data"].get("ad_spin_credits", 0)
            total_spins = free_left + ad_credits

            if total_spins > 0:
                log_yellow(f"Spinning {free_left} free and {ad_credits} credit spins now.")
                for _ in range(total_spins):
                    try:
                        res = api_spin_do(session, init_data, h)
                        if res.get("ok"):
                            amount = res["data"].get("amount", 0)
                            reward_type = res["data"].get("type", "unknown")
                            log_green(f"Spin result is {amount} {reward_type.upper()} rewarded.")
                            time.sleep(random.uniform(1.5, 3.0))
                        else:
                            log_red("Spin request was rejected by server.")
                            break
                    except Exception:
                        log_red("Failed to execute spin due to a network error.")
                        break
            else:
                log_yellow("No spins available at this time.")
        else:
            log_yellow("Spin feature is currently disabled or unavailable.")
    except Exception:
        log_red("Failed to process spin session due to a network error.")

    try:
        farm_res = api_farm_start(session, init_data, h)
        if farm_res.get("ok"):
            daily_limit = farm_res["data"].get("daily_limit", 0)
            remaining_farm = daily_limit - claims_today
            log_yellow(f"Farm claims today is {claims_today} out of {daily_limit} allowed.")
            for _ in range(remaining_farm):
                try:
                    claim_res = api_farm_claim(session, init_data, h)
                    if claim_res.get("ok"):
                        log_green("Farm reward claimed successfully.")
                        new_claims = claim_res["data"].get("claims_today", 0)
                        new_limit = claim_res["data"].get("daily_limit", daily_limit)
                        if new_claims >= new_limit:
                            log_yellow("Farm daily limit reached, not restarting.")
                            break
                        start_res = api_farm_start(session, init_data, h)
                        if start_res.get("ok"):
                            log_green("Farm session restarted successfully.")
                        else:
                            log_yellow("Farm could not be restarted.")
                            break
                    else:
                        log_yellow("Farm is not ready to claim yet.")
                        break
                except Exception:
                    log_red("Failed to claim farm reward due to a network error.")
                    break
        else:
            log_yellow("Farm returned an unexpected response from server.")
    except Exception:
        log_red("Failed to process farm claim due to a network error.")

    try:
        ad_status = api_ad_status(session, init_data, h)
        if not ad_status.get("ok"):
            log_red("Failed to retrieve ad status from server.")
            return
        ads_enabled = ad_status["data"].get("ads_enabled", False)

        if not ads_enabled:
            log_yellow("Ad feature is currently disabled on this server.")
        else:
            used = ad_status["data"].get("used", 0)
            limit = ad_status["data"].get("limit", 0)
            if used >= limit:
                log_yellow(f"Ad limit already reached at {used} out of {limit} today.")
            else:
                log_yellow(f"Starting ad session with {used} used out of {limit} daily limit.")
                while True:
                    ad_status = api_ad_status(session, init_data, h)
                    if not ad_status.get("ok"):
                        break
                    used = ad_status["data"].get("used", 0)
                    limit = ad_status["data"].get("limit", 0)
                    cd = ad_status["data"].get("cooldown_seconds", 0)

                    if used >= limit:
                        log_green(f"All {limit} ad slots completed for today.")
                        break

                    if cd > 0:
                        countdown(cd + 5, "Ad cooldown remaining")
                        continue

                    try:
                        start_res = None
                        for _ in range(3):
                            r = api_ad_start(session, init_data, h)
                            if r.get("ok"):
                                start_res = r
                                break
                            time.sleep(5)
                        if not start_res:
                            log_red("Ad start request was rejected by server after retries.")
                            break
                        sid = start_res["data"]["session_id"]
                        countdown(15, "Ad waiting")
                        complete_res = None
                        for _ in range(3):
                            r = api_ad_complete(session, init_data, sid, h)
                            if r.get("ok"):
                                complete_res = r
                                break
                            time.sleep(5)
                        if complete_res:
                            reward = complete_res["data"].get("reward", 0)
                            remaining = complete_res["data"].get("remaining", 0)
                            log_green(f"Ad completed with reward {reward} WIENER, {remaining} ads remaining.")
                        else:
                            log_red("Ad complete request was rejected by server after retries.")
                    except Exception:
                        log_red("Failed to process ad session due to a network error.")
                        break
    except Exception:
        log_red("Failed to initialize ad processing due to a network error.")

    try:
        wd_status = api_wd_status(session, init_data, h)
        if not wd_status.get("ok"):
            log_red("Failed to retrieve withdrawal ad status from server.")
            return
        count = wd_status["data"].get("count", 0)
        required = wd_status["data"].get("required", 0)
        unlocked = wd_status["data"].get("unlocked", False)

        if unlocked or count >= required:
            log_green(f"Withdrawal ad requirement already met at {count} out of {required}.")
        else:
            log_yellow(f"Processing withdrawal ads, currently at {count} out of {required} required.")
            while True:
                wd_status = api_wd_status(session, init_data, h)
                if not wd_status.get("ok"):
                    break
                count = wd_status["data"].get("count", 0)
                required = wd_status["data"].get("required", 0)
                unlocked = wd_status["data"].get("unlocked", False)

                if unlocked or count >= required:
                    log_green(f"Withdrawal ad requirement completed at {count} out of {required}.")
                    break

                try:
                    start_res = api_wd_ad_start(session, init_data, h)
                    if not start_res.get("ok"):
                        log_red("Withdrawal ad start was rejected by server.")
                        break
                    sid = start_res["data"]["session_id"]
                    countdown(15, "Withdrawal ad waiting")
                    claim_res = api_wd_ad_claim(session, init_data, sid, h)
                    if claim_res.get("ok"):
                        new_count = claim_res["data"].get("count", count)
                        log_green(f"Withdrawal ad credited, progress is now {new_count} out of {required}.")
                        time.sleep(random.uniform(2.0, 4.0))
                    else:
                        log_red("Withdrawal ad claim was rejected by server.")
                        break
                except Exception:
                    log_red("Failed to process withdrawal ad due to a network error.")
                    break
    except Exception:
        log_red("Failed to initialize withdrawal ad processing due to a network error.")


def main():
    show_banner(MY_PROJECT)
    cfg = load_config()
    sleep_seconds = cfg.get("settings", {}).get("sleep_seconds", 3600)
    accounts = load_initdata()
    proxies = load_proxies()
    device_cache = load_device_cache()

    log_yellow(f"Loaded {len(accounts)} accounts from data.txt.")

    cycle = 1
    while True:
        for idx, init_data in enumerate(accounts):
            if idx > 0:
                print()
            process_account(init_data, get_proxy_for_index(proxies, idx), device_cache)

        log_green(f"Cycle number {cycle} completed for all accounts.")
        cycle += 1
        countdown(sleep_seconds, "Next cycle starts in")
        show_banner(MY_PROJECT)
        log_yellow(f"Loaded {len(accounts)} accounts from data.txt.")


if __name__ == "__main__":
    main()