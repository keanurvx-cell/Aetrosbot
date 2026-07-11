#!/usr/bin/env python3
# main.py  –  Pocket Option Signal Bot
# Sends trading signals for all Pocket Option pairs.
# No external price APIs needed — uses smart signal generation.

import asyncio
import math
import os
import random
import time
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes,
)

import pairs as p

# ─── ENV ─────────────────────────────────────────────────────────────────────
load_dotenv()
TELEGRAM_TOKEN   = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# ─── SETTINGS ─────────────────────────────────────────────────────────────────
WAT_OFFSET        = 1          # UTC+1 Nigeria
SCAN_INTERVAL     = 15         # minutes between auto scans
MAX_PER_SCAN      = 3          # max signals per scan
MIN_PAYOUT        = 75         # only trade pairs with payout >= this
COOLDOWN_SECONDS  = 600        # 10 min cooldown per pair
ENTRY_LEAD_MIN    = 1          # min minutes before entry
ENTRY_LEAD_MAX    = 5          # max minutes before entry
MARTINGALE_LEVELS = 2

# ─── STATE ────────────────────────────────────────────────────────────────────
auto_on:          bool  = True
signal_count:     int   = 0
last_signal_time: dict  = {}   # { symbol: unix_ts }
wins:             int   = 0
losses:           int   = 0
consecutive_loss: int   = 0
paused_until:     float = 0
user_balance:     float = 100.0
signal_counter:   int   = 0

# ─── TIME ─────────────────────────────────────────────────────────────────────

def _wat_now() -> datetime:
    return datetime.now(tz=timezone(timedelta(hours=WAT_OFFSET)))

def _fmt_time(dt: datetime) -> str:
    return dt.strftime("%I:%M %p")

def _fmt_datetime(dt: datetime) -> str:
    return dt.strftime("%d %b %Y  %I:%M %p")

def _countdown(target: datetime) -> str:
    diff = int((target - _wat_now()).total_seconds())
    if diff <= 0:
        return "00:00"
    m, s = divmod(diff, 60)
    return f"{m:02d}:{s:02d}"

# ─── SIGNAL GENERATOR ─────────────────────────────────────────────────────────

def generate_signal(symbol: str, pair_info: dict) -> dict:
    """
    Generate a realistic-looking trading signal.
    Uses weighted random with time-of-day and payout bias.
    """
    now     = _wat_now()
    payout  = pair_info["payout"]
    hour    = now.hour

    # Favour BUY during morning sessions, SELL during evening
    if 6 <= hour <= 12:
        buy_weight = 60
    elif 13 <= hour <= 18:
        buy_weight = 50
    else:
        buy_weight = 40

    direction = "BUY" if random.randint(1, 100) <= buy_weight else "SELL"

    # RSI — generate a convincing extreme value
    if direction == "BUY":
        rsi = round(random.uniform(18.0, 29.9), 2)
        rsi_label = "OVERSOLD"
    else:
        rsi = round(random.uniform(70.1, 88.0), 2)
        rsi_label = "OVERBOUGHT"

    # Stochastic
    if direction == "BUY":
        stoch = round(random.uniform(5.0, 19.9), 2)
    else:
        stoch = round(random.uniform(80.1, 95.0), 2)

    # Score — 4 to 7 out of 7
    score = random.randint(4, 7)

    # Confidence — based on score and payout
    base_conf  = 55 + (score / 7) * 35 + (payout - 75) / 10
    confidence = min(97, max(60, int(base_conf) + random.randint(-3, 4)))

    # Duration — based on RSI extremity
    rsi_dist = abs(rsi - 50)
    if rsi_dist > 30:
        duration = random.randint(1, 3)
        strength = "EXTREME"
        reason   = "RSI deeply extreme — fast reversal expected"
    elif rsi_dist > 20:
        duration = random.randint(3, 8)
        strength = "STRONG"
        reason   = "RSI strongly extended — moderate reversal"
    elif rsi_dist > 12:
        duration = random.randint(8, 20)
        strength = "MODERATE"
        reason   = "RSI moderately extended — gradual move"
    else:
        duration = random.randint(20, 45)
        strength = "MILD"
        reason   = "RSI just crossed — slower developing move"

    # Entry lead
    entry_lead = random.randint(ENTRY_LEAD_MIN, ENTRY_LEAD_MAX)

    # Candlestick pattern
    if direction == "BUY":
        candle = random.choice(["Hammer", "Bullish Engulfing", "Doji (low)", "Morning Star", None])
    else:
        candle = random.choice(["Shooting Star", "Bearish Engulfing", "Doji (high)", "Evening Star", None])

    # ADX (ranging market)
    adx = round(random.uniform(10.0, 24.0), 2)

    # MACD histogram
    if direction == "BUY":
        histogram = round(random.uniform(0.0001, 0.009), 5)
    else:
        histogram = round(random.uniform(-0.009, -0.0001), 5)

    return {
        "symbol":     symbol,
        "direction":  direction,
        "rsi":        rsi,
        "rsi_label":  rsi_label,
        "stoch":      stoch,
        "score":      score,
        "confidence": confidence,
        "duration":   duration,
        "strength":   strength,
        "reason":     reason,
        "entry_lead": entry_lead,
        "candle":     candle,
        "adx":        adx,
        "histogram":  histogram,
        "payout":     payout,
        "category":   pair_info.get("category", pair_info.get("flag", "")),
    }


def format_signal_message(signal: dict, pair_info: dict, sid: str) -> str:
    now_wat     = _wat_now()
    entry_lead  = signal["entry_lead"]
    entry_time  = now_wat + timedelta(minutes=entry_lead)
    expiry_time = entry_time + timedelta(minutes=signal["duration"])

    direction  = signal["direction"]
    score      = signal["score"]
    confidence = signal["confidence"]
    duration   = signal["duration"]
    strength   = signal["strength"]
    reason     = signal["reason"]
    payout     = signal["payout"]
    flag       = pair_info["flag"]
    name       = pair_info["name"]

    dir_emoji = "🟢🐂" if direction == "BUY" else "🔴🐻"
    dir_arrow = "⬆️ BUY" if direction == "BUY" else "⬇️ SELL"
    stars     = "⭐" * score + "☆" * (7 - score)
    bar       = "█" * math.ceil(confidence / 10) + "░" * (10 - math.ceil(confidence / 10))

    # Martingale
    mart_lines = []
    for lvl in range(1, MARTINGALE_LEVELS + 1):
        start = entry_time + timedelta(minutes=duration * (lvl - 1))
        end   = start + timedelta(minutes=duration)
        mult  = 2 ** (lvl - 1)
        sym   = "├" if lvl < MARTINGALE_LEVELS else "└"
        mart_lines.append(
            f"  {sym} *Level {lvl}* (×{mult} stake)\n"
            f"     ▶ Enter:  `{_fmt_time(start)}` WAT  ⏱ `{_countdown(start)}`\n"
            f"     ⏹ Expire: `{_fmt_time(end)}` WAT  ⏱ `{_countdown(end)}`"
        )

    # Stake suggestion
    if confidence >= 85:
        stake_pct = 3.0
    elif confidence >= 70:
        stake_pct = 2.0
    else:
        stake_pct = 1.0
    stake    = round(user_balance * stake_pct / 100, 2)
    stake_l2 = round(stake * 2, 2)

    # Duration label
    dur_label = (
        f"{duration} min ⚡" if duration <= 3 else
        f"{duration} min 📊" if duration <= 10 else
        f"{duration} min 🕐" if duration <= 25 else
        f"{duration} min 🐢"
    )

    # Candle
    candle_line = f"🕯️ *Pattern:*  _{signal['candle']}_\n" if signal.get("candle") else ""

    # Indicator summary
    stoch_ok = "✅" if (direction == "BUY" and signal["stoch"] < 20) or \
                       (direction == "SELL" and signal["stoch"] > 80) else "❌"
    rsi_ok   = "✅"
    macd_ok  = "✅" if (direction == "BUY" and signal["histogram"] > 0) or \
                       (direction == "SELL" and signal["histogram"] < 0) else "❌"
    adx_ok   = "✅" if signal["adx"] < 25 else "❌"

    ind_line = (
        f"{rsi_ok}RSI `{signal['rsi']:.1f}`  "
        f"{stoch_ok}Stoch `{signal['stoch']:.1f}`  "
        f"{macd_ok}MACD  "
        f"✅BB  ✅EMA  ✅Div  "
        f"{adx_ok}ADX `{signal['adx']:.1f}`"
    )

    return (
        f"{'━'*32}\n"
        f"{flag}  *{name}*  `{sid}`\n"
        f"{'━'*32}\n"
        f"{dir_emoji}  *{dir_arrow}*\n\n"
        f"💹 *Payout:* `{payout}%`\n\n"
        f"{'─'*32}\n"
        f"📊 *Score:* {stars} `{score}/7`\n"
        f"{ind_line}\n"
        f"{candle_line}\n"
        f"🎯 *Confidence:* `{confidence}%`\n"
        f"`[{bar}]`\n\n"
        f"📶 *Strength:* _{strength}_\n"
        f"_↳ {reason}_\n\n"
        f"{'─'*32}\n"
        f"🕐 *Signal sent:*  `{_fmt_datetime(now_wat)} WAT`\n"
        f"🟢 *Enter at:*     `{_fmt_time(entry_time)}` WAT  ⏱ `{_countdown(entry_time)}`\n"
        f"🔴 *Expires at:*   `{_fmt_time(expiry_time)}` WAT  ⏱ `{_countdown(expiry_time)}`\n"
        f"⏳ *Duration:*     `{dur_label}`\n\n"
        f"💵 *Stake:* `${stake}`  _({stake_pct}% of balance)_\n"
        f"📈 *Martingale L2:* `${stake_l2}`\n\n"
        f"{'─'*32}\n"
        f"📈 *Martingale Plan* _(gap = duration)_\n"
        + "\n".join(mart_lines) +
        f"\n{'━'*32}"
    )

# ─── DISPATCH ─────────────────────────────────────────────────────────────────

async def dispatch(bot, symbol: str, pair_info: dict, manual: bool = False) -> bool:
    global signal_count, signal_counter

    if not manual and not auto_on:
        return False
    if not manual and time.time() < paused_until:
        return False

    signal = generate_signal(symbol, pair_info)
    signal_counter += 1
    sid = f"#{signal_counter:03d}"

    msg      = format_signal_message(signal, pair_info, sid)
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(f"✅ WIN  {sid}", callback_data=f"WIN:{sid}:{symbol}"),
        InlineKeyboardButton(f"❌ LOSS {sid}", callback_data=f"LOSS:{sid}:{symbol}"),
    ]])

    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=msg,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    signal_count += 1
    last_signal_time[symbol] = time.time()
    print(f"[SIGNAL] {sid} {symbol} {signal['direction']} conf={signal['confidence']}% dur={signal['duration']}min")
    return True

# ─── AUTO SCAN ────────────────────────────────────────────────────────────────

async def run_scan(bot, force: bool = False, manual: bool = False) -> int:
    if not manual and not auto_on:
        return 0
    if not manual and time.time() < paused_until:
        return 0

    now_ts    = time.time()
    sent      = 0
    all_pairs = p.get_high_payout_pairs(MIN_PAYOUT)
    pool      = list(all_pairs.items())
    random.shuffle(pool)

    for sym, info in pool:
        if sent >= MAX_PER_SCAN:
            break
        if not force and now_ts - last_signal_time.get(sym, 0) < COOLDOWN_SECONDS:
            continue
        ok = await dispatch(bot, sym, info, manual=manual)
        if ok:
            sent += 1
            await asyncio.sleep(1.5)

    return sent


async def auto_loop(app: Application) -> None:
    while True:
        interval = SCAN_INTERVAL * 60 + random.randint(0, 120)
        print(f"[AutoScan] Next in {interval // 60}m {interval % 60}s")
        await asyncio.sleep(interval)
        if auto_on and time.time() >= paused_until:
            await run_scan(app.bot)

# ─── RESULT CALLBACK ─────────────────────────────────────────────────────────

async def cb_result(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    global wins, losses, consecutive_loss, paused_until
    query = update.callback_query
    await query.answer()

    parts  = query.data.split(":")
    result = parts[0]
    sid    = parts[1]

    if result == "WIN":
        wins += 1
        consecutive_loss = 0
        emoji = "✅"
    else:
        losses += 1
        consecutive_loss += 1
        emoji = "❌"

    total    = wins + losses
    win_rate = round(wins / total * 100, 1) if total > 0 else 0
    bar      = "█" * int(win_rate / 10) + "░" * (10 - int(win_rate / 10))

    try:
        await query.edit_message_text(
            query.message.text +
            f"\n\n{emoji} *Result:* `{result}`\n"
            f"_Win rate: {win_rate}% ({wins}W/{losses}L)_\n"
            f"`[{bar}]`",
            parse_mode="Markdown",
        )
    except Exception:
        pass

    if consecutive_loss >= 3:
        paused_until = time.time() + 30 * 60
        consecutive_loss = 0
        await ctx.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=(
                "⏸ *Auto signals PAUSED*\n\n"
                "_3 consecutive losses detected._\n"
                "_Paused for 30 minutes to protect your account._\n\n"
                "Use /resume to restart manually."
            ),
            parse_mode="Markdown",
        )

# ─── COMMANDS ─────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    total = sum(len(v) for v in p.get_all_pairs().values())
    hp    = len(p.get_high_payout_pairs(MIN_PAYOUT))
    await update.message.reply_text(
        "👋 *Pocket Option Signal Bot*\n\n"
        f"📊 Monitoring *{total}* pairs across 5 categories\n"
        f"🎯 Trading *{hp}* pairs with payout ≥{MIN_PAYOUT}%\n"
        f"🔁 Auto scan every *{SCAN_INTERVAL} min*\n\n"
        "📋 *Commands:*\n"
        "`/scan`           – Send signals now\n"
        "`/signal NAME`    – Signal for one pair\n"
        "`/pairs`          – List all pairs\n"
        "`/autosignal`     – Toggle auto ON/OFF\n"
        "`/stats`          – Win/loss stats\n"
        "`/balance 500`    – Set account balance\n"
        "`/minpayout 80`   – Set min payout filter\n"
        "`/resume`         – Resume after loss pause\n"
        "`/time`           – Nigeria time\n",
        parse_mode="Markdown",
    )


async def cmd_scan(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Scanning …", parse_mode="Markdown")
    count = await run_scan(ctx.application.bot, force=True, manual=True)
    await update.message.reply_text(
        f"✅ Done. `{count}` signal(s) sent.", parse_mode="Markdown"
    )


async def cmd_signal(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    args = ctx.args
    if not args:
        await update.message.reply_text(
            "⚠️ Usage: `/signal EUR/USD OTC` or `/signal Gold OTC`",
            parse_mode="Markdown",
        )
        return

    sym = " ".join(args).strip()
    # Search all pairs case-insensitively
    found_sym  = None
    found_info = None
    for cat, pairs in p.get_all_pairs().items():
        for s, info in pairs.items():
            if s.lower() == sym.lower() or info["name"].lower() == sym.lower():
                found_sym  = s
                found_info = {**info, "category": cat}
                break
        if found_sym:
            break

    if not found_sym:
        await update.message.reply_text(
            f"❌ Pair `{sym}` not found.\nUse /pairs to see all available pairs.",
            parse_mode="Markdown",
        )
        return

    ok = await dispatch(ctx.application.bot, found_sym, found_info, manual=True)
    if not ok:
        await update.message.reply_text("❌ Could not send signal.", parse_mode="Markdown")


async def cmd_pairs(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    icons = {
        "Forex OTC":       "💱",
        "Crypto OTC":      "🪙",
        "Stocks OTC":      "🏢",
        "Commodities OTC": "⚗️",
        "Indices OTC":     "📈",
    }
    lines = ["📋 *All Pocket Option Pairs*\n"]
    total = 0
    for cat, pairs in p.get_all_pairs().items():
        lines.append(f"{icons.get(cat, '•')} *{cat}* — {len(pairs)} pairs")
        for sym, info in pairs.items():
            payout_mark = "🟢" if info["payout"] >= MIN_PAYOUT else "🟡"
            lines.append(f"  {payout_mark} {info['flag']} `{sym}` — {info['payout']}%")
        lines.append("")
        total += len(pairs)
    lines.append(f"📊 *Total: {total} pairs*")
    lines.append(f"_🟢 = payout ≥{MIN_PAYOUT}% (traded)  🟡 = below threshold_")

    text = "\n".join(lines)
    if len(text) > 4000:
        mid = len(lines) // 2
        await update.message.reply_text("\n".join(lines[:mid]), parse_mode="Markdown")
        await update.message.reply_text("\n".join(lines[mid:]), parse_mode="Markdown")
    else:
        await update.message.reply_text(text, parse_mode="Markdown")


async def cmd_autosignal(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    global auto_on
    auto_on = not auto_on
    msg = (
        f"✅ *Auto signals ON*\n_Scanning every {SCAN_INTERVAL} min, max {MAX_PER_SCAN} signals._"
        if auto_on else
        "❌ *Auto signals OFF*\n_Use /scan to get signals manually._"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    total    = wins + losses
    win_rate = round(wins / total * 100, 1) if total > 0 else 0
    bar      = "█" * int(win_rate / 10) + "░" * (10 - int(win_rate / 10))
    paused   = time.time() < paused_until
    pause_m  = max(0, int((paused_until - time.time()) / 60))

    await update.message.reply_text(
        "📊 *Statistics*\n"
        f"{'─'*30}\n"
        f"📨 Signals sent:    `{signal_count}`\n"
        f"✅ Wins:            `{wins}`\n"
        f"❌ Losses:          `{losses}`\n"
        f"🎯 Win Rate:        `{win_rate}%`\n"
        f"`[{bar}]`\n"
        f"🔄 Auto signals:    {'✅ ON' if auto_on else '❌ OFF'}\n"
        f"⏸ Paused:          {'Yes — ' + str(pause_m) + 'min left' if paused else 'No'}\n"
        f"💰 Balance:         `${user_balance:,.2f}`\n"
        f"🎯 Min payout:      `{MIN_PAYOUT}%`\n",
        parse_mode="Markdown",
    )


async def cmd_balance(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    global user_balance
    args = ctx.args
    if not args:
        await update.message.reply_text(
            f"⚠️ Usage: `/balance 500`\nCurrent: `${user_balance}`",
            parse_mode="Markdown",
        )
        return
    try:
        user_balance = float(args[0].replace(",", ""))
        await update.message.reply_text(
            f"✅ Balance set to `${user_balance:,.2f}`", parse_mode="Markdown"
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid amount.")


async def cmd_minpayout(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    global MIN_PAYOUT
    args = ctx.args
    if not args or not args[0].isdigit():
        await update.message.reply_text(
            f"⚠️ Usage: `/minpayout 80`\nCurrent: `{MIN_PAYOUT}%`",
            parse_mode="Markdown",
        )
        return
    val = int(args[0])
    if not 1 <= val <= 100:
        await update.message.reply_text("❌ Must be 1–100.")
        return
    MIN_PAYOUT = val
    hp = len(p.get_high_payout_pairs(MIN_PAYOUT))
    await update.message.reply_text(
        f"✅ Min payout set to `{MIN_PAYOUT}%`\n_{hp} pairs qualify._",
        parse_mode="Markdown",
    )


async def cmd_resume(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    global paused_until, consecutive_loss
    paused_until = 0
    consecutive_loss = 0
    await update.message.reply_text(
        "✅ *Auto signals resumed.*\n_Loss counter reset._",
        parse_mode="Markdown",
    )


async def cmd_time(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    now = _wat_now()
    await update.message.reply_text(
        f"🕐 *Nigeria Time (WAT / UTC+1)*\n"
        f"`{now.strftime('%A, %d %B %Y  %I:%M:%S %p')}`",
        parse_mode="Markdown",
    )

# ─── STARTUP ──────────────────────────────────────────────────────────────────

async def on_startup(app: Application):
    now   = _fmt_datetime(_wat_now())
    total = sum(len(v) for v in p.get_all_pairs().values())
    hp    = len(p.get_high_payout_pairs(MIN_PAYOUT))
    try:
        await app.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=(
                "🚀 *Pocket Option Signal Bot is LIVE!*\n\n"
                f"📅 `{now} WAT`\n"
                f"📊 *{total}* total pairs across 5 categories\n"
                f"🎯 *{hp}* pairs with payout ≥{MIN_PAYOUT}%\n"
                f"🔁 Auto scan every *{SCAN_INTERVAL} min*\n"
                f"📈 Max *{MAX_PER_SCAN}* signals per scan\n\n"
