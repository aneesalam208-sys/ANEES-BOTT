import asyncio
import random
from pyrogram import Client, filters

# --- CONFIGURATION (5 BOT TOKENS) ---
BOT_TOKENS = [
    "8839857816:AAElwSCwt9pAgWT7_1YULFkRJGAm1tjp1BY",
    "8926833278:AAEyu2tvHAq_DnYwLxzNxDdzGVRjS-Tdurs",
    "8668406594:AAF609Rm3p-MKspUhFqgDJFRh8nD2xUYr1k",
    "8915398294:AAGHqXD67g0asuS3AxnsYBW5ZEqoc2ug6nk",
    "8085862626:AAFcm59X0aX-j6CpryjUdIHoXT4v3HVi2HA",
]

OWNER_ID = 5664545994  # Aapki Telegram Owner ID

# Multiple Clients initialization
apps = [
    Client(f"anees_bot_{i}", bot_token=token)
    for i, token in enumerate(BOT_TOKENS)
]

# Global variables
loops_running = {"nc": False, "spam": False, "reply": False}
delay_time = 2.0  # Default delay 2 seconds
thread_count = 5
reply_target = None  # Reply command ke liye target storage

# --- SPAM / NC TEXT VARIATIONS ---
NAME_VARIATIONS = [
    (
        "Aɴᴇᴇs Dᴀᴅᴅʏ Exɪᴛᴢ {target} Kɪ ᴍᴀᴀ"
        " Xʜᴏᴅᴋᴇ____________________________‽🚀"
    ),
    (
        "🔥 Aɴᴇᴇs Dᴀᴅᴅʏ Exɪᴛᴢ {target} Kɪ ᴍᴀᴀ"
        " Xʜᴏᴅᴋᴇ____________________________‽🚀"
    ),
    (
        "👑 Aɴᴇᴇs Dᴀᴅᴅʏ Exɪᴛᴢ {target} Kɪ ᴍᴀᴀ"
        " Xʜᴏᴅᴋᴇ____________________________‽🚀"
    ),
    (
        "⚡ Aɴᴇᴇs Dᴀᴅᴅʏ Exɪᴛᴢ {target} Kɪ ᴍᴀᴀ"
        " Xʜᴏᴅᴋᴇ____________________________‽🚀"
    ),
    (
        "💀 Aɴᴇᴇs Dᴀᴅᴅʏ Exɪᴛᴢ {target} Kɪ ᴍᴀᴀ"
        " Xʜᴏᴅᴋᴇ____________________________‽🚀"
    ),
    (
        "🚀 Aɴᴇᴇs Dᴀᴅᴅʏ Exɪᴛᴢ {target} Kɪ ᴍᴀᴀ"
        " Xʜᴏᴅᴋᴇ____________________________‽🚀"
    ),
    (
        "🎯 Aɴᴇᴇs Dᴀᴅᴅʏ Exɪᴛᴢ {target} Kɪ ᴍᴀᴀ"
        " Xʜᴏᴅᴋᴇ____________________________‽🚀"
    ),
    (
        "⚠️ Aɴᴇᴇs Dᴀᴅᴅʏ Exɪᴛᴢ {target} Kɪ ᴍᴀᴀ"
        " Xʜᴏᴅᴋᴇ____________________________‽🚀"
    ),
    (
        "💥 Aɴᴇᴇs Dᴀᴅᴅʏ Exɪᴛᴢ {target} Kɪ ᴍᴀᴀ"
        " Xʜᴏᴅᴋᴇ____________________________‽🚀"
    ),
    (
        "🌪️ Aɴᴇᴇs Dᴀᴅᴅʏ Exɪᴛᴢ {target} Kɪ ᴍᴀᴀ"
        " Xʜᴏᴅᴋᴇ____________________________‽🚀"
    ),
]

# --- REPLY TEXT VARIATIONS ---
REPLY_VARIATIONS = [
    "𝐀𝐍𝐄𝐄𝐒 / 𝐌𝐀𝐇𝐀𝐑𝐀𝐉𝐀 𝐍𝐄 {target} 𝐊𝐈 𝐌𝐀𝐀 𝐂𝐇𝐎𝐃 𝐃𝐀𝐀𝐋𝐈 👑🔥",
    "⚡ 𝐀𝐍𝐄𝐄𝐒 / 𝐌𝐀𝐇𝐀𝐑𝐀𝐉𝐀 𝐍𝐄 {target} 𝐊𝐈 𝐌𝐀𝐀 𝐂𝐇𝐎𝐃 𝐃𝐀𝐀𝐋𝐈 🚀",
    "💀 𝐀𝐍𝐄𝐄𝐒 / 𝐌𝐀𝐇𝐀𝐑𝐀𝐉𝐀 𝐍𝐄 {target} 𝐊𝐈 𝐌𝐀𝐀 𝐂𝐇𝐎𝐃 𝐃𝐀𝐀𝐋𝐈 🌪️",
    "🔥 𝐀𝐍𝐄𝐄𝐒 / 𝐌𝐀𝐇𝐀𝐑𝐀𝐉𝐀 𝐍𝐄 {target} 𝐊𝐈 𝐌𝐀𝐀 𝐂𝐇𝐎𝐃 𝐃𝐀𝐀𝐋𝐈 🎯",
    "👑 𝐀𝐍𝐄𝐄𝐒 / 𝐌𝐀𝐇𝐀𝐑𝐀𝐉𝐀 𝐍𝐄 {target} 𝐊𝐈 𝐌𝐀𝐀 𝐂𝐇𝐎𝐃 𝐃𝐀𝐀𝐋𝐈 💥",
]


# Handlers registration for all bot clients
def register_handlers(app):

  @app.on_message(filters.command("start") & filters.user(OWNER_ID))
  async def start_command(client, message):
    menu_text = (
        "𓆩 𝐁𝐎𝐓 6 𓆪 - 👑 【 𝑨𝑵𝑬𝑬𝑺 𝑩𝑯𝑨𝑮𝑾𝑨𝑨𝑵 𝑻𝑬𝑳𝑬𝑮𝑹𝑨𝑴 𝑮𝑶𝑫 】 👑\n\n"
        "𝐂𝐨𝐦𝐦𝐚𝐧𝑑𝐬:\n"
        "/target <name> - NC + SPAM together with threads!\n"
        "/nc <name> - Name change LOOP (with threads)\n"
        "/spam <target> - Spam LOOP (with threads)\n"
        "/reply <target> - Reply to every message LOOP!\n\n"
        "/delay <seconds> - Set delay (default: 2)\n"
        "/threads <1-50> - Set threads for NC + SPAM\n\n"
        "/stopnc - Stop name change loop\n"
        "/stopspam - Stop spam loop\n"
        "/stopreply - Stop reply loop\n"
        "/stopall - Stop ALL loops\n\n"
        f"Current Delay: {delay_time}s | Threads: {thread_count}\n"
        "𝐀𝐥𝐥 𝐚𝐜𝐭𝐢𝐨𝐧𝐬 𝐫𝐮𝐧 𝐢𝐧 𝐋𝐎𝐎𝐏𝐒 ⚡\n"
        "𝐎𝐰𝐧𝐞𝐫 𝐎𝐧𝐥𝐲 🔒"
    )
    await message.reply_text(menu_text)

  @app.on_message(filters.command("delay") & filters.user(OWNER_ID))
  async def set_delay(client, message):
    global delay_time
    try:
      delay_time = float(message.command[1])
      await message.reply_text(f"✅ Delay set to {delay_time} seconds.")
    except IndexError:
      await message.reply_text("❌ Please provide seconds. Usage: `/delay 2`")

  @app.on_message(filters.command("threads") & filters.user(OWNER_ID))
  async def set_threads(client, message):
    global thread_count
    try:
      val = int(message.command[1])
      if 1 <= val <= 50:
        thread_count = val
        await message.reply_text(f"✅ Threads set to {thread_count}.")
      else:
        await message.reply_text("❌ Threads must be between 1 and 50.")
    except IndexError:
      await message.reply_text("❌ Usage: `/threads 10`")

  async def nc_worker(client, message, target):
    while loops_running["nc"]:
      try:
        text_template = random.choice(NAME_VARIATIONS)
        new_name = text_template.format(target=target)
        await client.update_profile(first_name=new_name)
        await asyncio.sleep(max(delay_time, 2))
      except Exception as e:
        print(e)

  async def spam_worker(client, message, target):
    while loops_running["spam"]:
      try:
        text_template = random.choice(NAME_VARIATIONS)
        spam_text = text_template.format(target=target)
        await message.reply_text(spam_text)
        await asyncio.sleep(delay_time)
      except Exception as e:
        print(e)

  @app.on_message(filters.group & ~filters.user(OWNER_ID))
  async def auto_reply_handler(client, message):
    global reply_target
    if loops_running["reply"] and reply_target:
      if message.from_user and (
          reply_target.lower() in message.from_user.first_name.lower()
          or (
              message.from_user.username
              and reply_target.lower() in message.from_user.username.lower()
          )
      ):
        try:
          text_template = random.choice(REPLY_VARIATIONS)
          reply_text = text_template.format(target=reply_target)
          await message.reply_text(reply_text)
          await asyncio.sleep(delay_time)
        except Exception as e:
          print(e)

  @app.on_message(filters.command("nc") & filters.user(OWNER_ID))
  async def start_nc(client, message):
    if len(message.command) < 2:
      return await message.reply_text("❌ Usage: `/nc <name>`")
    target = " ".join(message.command[1:])
    loops_running["nc"] = True
    await message.reply_text(
        f"🚀 Name Change loop started with {thread_count} threads (Delay:"
        f" {delay_time}s)!"
    )
    tasks = [
        asyncio.create_task(nc_worker(client, message, target))
        for _ in range(thread_count)
    ]
    await asyncio.gather(*tasks)

  @app.on_message(filters.command("spam") & filters.user(OWNER_ID))
  async def start_spam(client, message):
    if len(message.command) < 2:
      return await message.reply_text("❌ Usage: `/spam <target>`")
    target = " ".join(message.command[1:])
    loops_running["spam"] = True
    await message.reply_text(
        f"🚀 Spam loop started with {thread_count} threads (Delay: {delay_time}s)!"
    )
    tasks = [
        asyncio.create_task(spam_worker(client, message, target))
        for _ in range(thread_count)
    ]
    await asyncio.gather(*tasks)

  @app.on_message(filters.command("target") & filters.user(OWNER_ID))
  async def start_target(client, message):
    if len(message.command) < 2:
      return await message.reply_text("❌ Usage: `/target <name>`")
    target = " ".join(message.command[1:])
    loops_running["nc"] = True
    loops_running["spam"] = True
    await message.reply_text(
        f"👑 TARGET (NC + SPAM) started with {thread_count} threads (Delay:"
        f" {delay_time}s)!"
    )
    tasks = [
        asyncio.create_task(nc_worker(client, message, target)),
        asyncio.create_task(spam_worker(client, message, target)),
    ]
    await asyncio.gather(*tasks)

  @app.on_message(filters.command("reply") & filters.user(OWNER_ID))
  async def start_reply(client, message):
    global reply_target
    if len(message.command) < 2:
      return await message.reply_text("❌ Usage: `/reply <target>`")
    reply_target = " ".join(message.command[1:])
    loops_running["reply"] = True
    await message.reply_text(
        f"🎯 Auto-reply loop activated against target: {reply_target}"
    )

  @app.on_message(filters.command("stopnc") & filters.user(OWNER_ID))
  async def stop_nc(client, message):
    loops_running["nc"] = False
    await message.reply_text("🛑 Name Change loop stopped.")

  @app.on_message(filters.command("stopspam") & filters.user(OWNER_ID))
  async def stop_spam(client, message):
    loops_running["spam"] = False
    await message.reply_text("🛑 Spam loop stopped.")

  @app.on_message(filters.command("stopreply") & filters.user(OWNER_ID))
  async def stop_reply(client, message):
    loops_running["reply"] = False
    await message.reply_text("🛑 Auto-reply loop stopped.")

  @app.on_message(filters.command("stopall") & filters.user(OWNER_ID))
  async def stop_all(client, message):
    for key in loops_running:
      loops_running[key] = False
    await message.reply_text("🛑 All loops stopped successfully!")


# Sabhi bots par handlers apply karo
for app in apps:
  register_handlers(app)


# Main function to run all bots together concurrently
async def main():
  await asyncio.gather(*(app.start() for app in apps))
  print("🔥 All 5 Bots Started Successfully 24/7 Ready!")
  await asyncio.Event().wait()


if __name__ == "__main__":
  asyncio.run(main())
