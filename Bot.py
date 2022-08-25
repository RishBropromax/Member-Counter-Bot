import os, logging, asyncio

from telethon import Button

from telethon import TelegramClient, events

from telethon.tl.types import ChannelParticipantAdmin

from telethon.tl.types import ChannelParticipantCreator

from telethon.tl.functions.channels import GetParticipantRequest

from telethon.errors import UserNotParticipantError

logging.basicConfig(

    level=logging.INFO,

    format='%(name)s - [%(levelname)s] - %(message)s'

)

LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))

api_hash = os.environ.get("API_HASH")

bot_token = os.environ.get("TOKEN")

client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

spam_chats = []

@client.on(events.NewMessage(pattern="/allStart"))

async def start(event):

  await event.reply(

    "🌹🔥🇱🇰 **Member Counter Bot**, I can mention almost all members in group or channel.",

    link_preview=False,

    buttons=(

      [

        Button.url('📣 Channel', 'https://t.me/CatXGirlNews'),

        Button.url('📦 Source', 'https://github.com/RishbroProMax/Member-Counter-Bot')

      ]

    )

  )

@client.on(events.NewMessage(pattern="/allhelp"))

async def help(event):

  helptext = "**Mention Help Menu of Cat X Girl **\n\nCommand: @all\n 🔥🇱🇰 You can use this command with text what you want to mention others.\n`Example: @all Im Member Counter Bot🌹!`\nYou can you this command as a reply to any message. Bot will tag users to that replied messsage.\n\nFollow [@RishbroProMax](https://github.com/RishbroProMax) on Github"

  await event.reply(

    helptext,

    link_preview=False,

    buttons=(

      [

        Button.url('📣 Channel', 'https://t.me/CatXGirlNews'),

        Button.url('📦 Source', 'https://github.com/RishbroProMax/Cat-X-Girl-Bot')

      

    

  

@client.on(events.NewMessage(pattern="@all"))

async def mentionall(event):

  chat_id = event.chat_id

  if event.is_private:

    return await event.respond("This command can be use in groups and channels!")

  

  is_admin = False

  try:

    partici_ = await client(GetParticipantRequest(

      event.chat_id,

      event.sender_id

    ))

  except UserNotParticipantError:

    is_admin = False

  else:

    if (

      isinstance(

        partici_.participant,

        (

          ChannelParticipantAdmin,

          ChannelParticipantCreator

        )

      )

    ):

      is_admin = True

  if not is_admin:

    return await event.respond("Only admins can mention all!")

  

  if event.pattern_match.group(1) and event.is_reply:

    return await event.respond("Give me one argument!")

  elif event.pattern_match.group(1):

    mode = "text_on_cmd"

    msg = event.pattern_match.group(1)

  elif event.is_reply:

    mode = "text_on_reply"

    msg = await event.get_reply_message()

    if msg == None:

        return await event.respond("🇱🇰 I can't mention members for older messages! (messages which are sent before I'm added to group)__")

  else:

    return await event.respond("🌹 Reply to a message or give me some text to mention others!__")

  

  spam_chats.append(chat_id)

  usrnum = 0

  usrtxt = ''

  async for usr in client.iter_participants(chat_id):

    if not chat_id in spam_chats:

      break

    usrnum += 1

    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "

    if usrnum == 5:

      if mode == "text_on_cmd":

        txt = f"{usrtxt}\n\n{msg}"

        await client.send_message(chat_id, txt)

      elif mode == "text_on_reply":

        await msg.reply(usrtxt)

      await asyncio.sleep(2)

      usrnum = 0

      usrtxt = ''

  try:

    spam_chats.remove(chat_id)

  except:

    pass

@client.on(events.NewMessage(pattern="/cancel"))

async def cancel_spam(event):

  if not event.chat_id in spam_chats:

    return await event.respond('🔥 There is no proccess on going...__')

  else:

    try:

      spam_chats.remove(event.chat_id)

    except:

      pass

    return await event.respond('🌹🔥 Stopped 🌹🔥')

print(">> Mention Filter is Started <<")

client.run_until_disconnected()
