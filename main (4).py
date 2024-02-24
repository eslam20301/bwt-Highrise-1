from highrise import (
    BaseBot,
    ChatEvent,
    Highrise,
    __main__,
    UserJoinedEvent,
    UserLeftEvent,
)
from highrise.models import (
    AnchorPosition,
    ChannelEvent,
    ChannelRequest,
    ChatEvent,
    ChatRequest,
    CurrencyItem,
    EmoteEvent,
    EmoteRequest,
    Error,
    FloorHitRequest,
    GetRoomUsersRequest,
    GetWalletRequest,
    IndicatorRequest,
    Item,
    Position,
    Reaction,
    ReactionEvent,
    ReactionRequest,
    SessionMetadata,
    TeleportRequest,
    TipReactionEvent,
    User,
    UserJoinedEvent,
    UserLeftEvent,
)
from asyncio import run as arun
from webserver import keep_alive
import requests
import random
import asyncio
import os
import importlib
class BotDefinition:
    def __init__(self, bot, room_id, api_token):
        self.bot = bot
        self.room_id = room_id
        self.api_token = api_token

class Bot(BaseBot):
    
    async def on_start(self, SessionMetadata: SessionMetadata) -> None:
        try:
            await self.highrise.walk_to(Position(21., -1., 18.1, "FrontLeft"))
            await self.highrise.chat("Reconnected...")
        except Exception as e:
            print(f"error : {e}")

    async def on_reaction(self, user: User, reaction: Reaction, receiver: User) -> None:
        text_to_emoji = {
        "wink": "😉",
        "wave": "👋",
        "thumbs": "👍",
        "heart": "❤️",
        "clap": "👏",
        }
        await self.highrise.chat(f"\n{user.username} {text_to_emoji[reaction]} {receiver.username}")

    async def on_user_join(self, user: User) -> None:
        try:
            print(f"{user.username} Joined Room.")
            wm = [
            'welcome to party and vides FOLLOW @zandexprime and hosts hope u enjoy the party, pls tag us at #primexshadow and have a great time. ,!',
            ]
            rwm = random.choice(wm)
            await self.highrise.send_whisper(user.id, f"Hey @{user.username}\n{rwm}")
            await self.highrise.send_whisper(user.id, f"\n[📢] use !help or -help for codes. Show your gratitude by tipping the jar!\n\n~ ")
            face = ["FrontRight","FrontLeft"]
            fp = random.choice(face)
            #Change co-ordinates according to your room .
            
            __ = random.choice(_)
            await self.highrise.teleport(user.id, __)
        except Exception as e:
            print(f"error : {e}")
            
    async def on_chat(self, user: User, message: str):
        try:
            _bid = "" #Bot user.id here
            _id = f"1_on_1:{_bid}:{user.id}"
            _idx = f"1_on_1:{user.id}:{_bid}"
            _rid = "64e511e2467eed157d5122df" #Room ID Here
            if message.lower().lstrip().startswith(("!invite", "-invite")):
                parts = message[1:].split()
                args = parts[1:]

                if len(args) < 1:
                    await self.highrise.send_whisper(user.id, "\nUsage: !invite <@username> or -invite <@username> This command will send room invite to targeted username. if they ever interact with our bot in past\n • Example: !invite @zandexprime")
                    return
                elif args[0][0] != "@":
                    await self.highrise.send_whisper(user.id, f"Invalid user format. Please use '@username'.")
                    return

                url = f"https://webapi.highrise.game/users?&username={args[0][1:]}&sort_order=asc&limit=1"
                response = requests.get(url)
                data = response.json()
                users = data['users']
                
                for user in users:
                    user_id = user['user_id']
                    __id = f"1_on_1:{_bid}:{user_id}"
                    __idx = f"1_on_1:{user_id}:{_bid}"
                    __rid = "64e511e2467eed157d5122df" #Room ID Here
                    try:
                        await self.highrise.send_message(__id, "Join Room", "invite", __rid)
                    except:
                        await self.highrise.send_message(__idx, "Join Room", "invite", __rid)

            if message.lower().lstrip().startswith(("-help", "!help")):
                await self.highrise.chat(f"\nHere are some commands:\n • !emote or -emote\n • !invite or -invite\n • !feedback\n • couple/friendly command\n   !flirt @username\n   !fight @username \n   !rock @username\n   Example : !flirt @zandexprime\n\nLeave a message to @zandexprime for any further assistance.")

            if message.lower().lstrip().startswith("!feedback"):
                try:
                    await self.highrise.send_message(_id, "• [ Submit Feedback ]\nThank you for joining our room! We value your feedback. Please share your feedback/suggestions with @fir3xd_ to enhance our environment. Your input is valuable and will help us improve.\n\nHave a wonderful day/night!", "text")
                except:
                    await self.highrise.send_message(_idx, "• [ Submit Feedback ]\nThank you for joining our room! We value your feedback. Please share your feedback/suggestions with @fir3xd_ to enhance our environment. Your input is valuable and will help us improve.\n\nHave a wonderful day/night!", "text")
                    
            if message.lower().lstrip().startswith(("-emote", "!emote")):
                await self.highrise.send_whisper(user.id, "\nEmote can be used with just typing EMOTE NAME in our room. Here's an example of emote use\n  casual\n  fashionista\n  floating\n\nand all other emotes just say name in room of any emote")
                await self.highrise.send_whisper(user.id, "\n• Note that these commands will only work in room called party 🎉 by @zandexprime some emotes may not work due to restrictions.")

            if message.lstrip().startswith(("!fight", "!hug", "!flirt")):
                response = await self.highrise.get_room_users()
                users = [content[0] for content in response.content]
                usernames = [user.username.lower() for user in users]
                parts = message[1:].split()
                args = parts[1:]
        
                if len(args) < 1:
                    await self.highrise.send_whisper(user.id, f"Usage: !{parts[0]} <@username>")
                    return
                elif args[0][0] != "@":
                    await self.highrise.send_whisper(user.id, f"Invalid user format. Please use '@username'.")
                    return
                elif args[0][1:].lower() not in usernames:
                    await self.highrise.send_whisper(user.id, f"{args[0][1:]} is not in the room.")
                    return
        
                user_id = next((u.id for u in users if u.username.lower() == args[0][1:].lower()), None)
                if not user_id:
                    await self.highrise.send_whisper(user.id, f"User {args[0][1:]} not found")
                    return
        
                try:
                    if message.startswith("!fight"):
                        await self.highrise.chat(f"\n🥷 @{user.username} And @{args[0][1:]} Fighting Each Other Like Dummies")
                        await self.highrise.send_emote("emote-swordfight", user.id)
                        await self.highrise.send_emote("emote-swordfight", user_id)
                    elif message.startswith("!hug"):
                        await self.highrise.chat(f"\n🫂 @{user.username} And @{args[0][1:]} Hugging Each Other❤️")
                        await self.highrise.send_emote("emote-hug", user.id)
                        await self.highrise.send_emote("emote-hug", user_id)
                    elif message.startswith("!flirt"):
                        await self.highrise.chat(f"\n Hey @{user.username} And @{args[0][1:]} Flirting Each Other 😏❤️")
                        await self.highrise.send_emote("emote-lust", user.id)
                        await self.highrise.send_emote("emote-lust", user_id)
                except Exception as e:
                    print(f"An exception occurred[Due To {parts[0][1:]}]: {e}")

            if message == "-dress":
                shirt = ["shirt-n_starteritems2019tankwhite", "shirt-n_starteritems2019tankblack", "shirt-n_starteritems2019raglanwhite", "shirt-n_starteritems2019raglanblack", "shirt-n_starteritems2019pulloverwhite", "shirt-n_starteritems2019pulloverblack", "shirt-n_starteritems2019maletshirtwhite", "shirt-n_starteritems2019maletshirtblack", "shirt-n_starteritems2019femtshirtwhite", "shirt-n_starteritems2019femtshirtblack", "shirt-n_room32019slouchyredtrackjacket", "shirt-n_room32019malepuffyjacketgreen", "shirt-n_room32019longlineteesweatshirtgrey", "shirt-n_room32019jerseywhite", "shirt-n_room32019hoodiered", "shirt-n_room32019femalepuffyjacketgreen", "shirt-n_room32019denimjackethoodie", "shirt-n_room32019croppedspaghettitankblack", "shirt-n_room22109plaidjacket", "shirt-n_room22109denimjacket", "shirt-n_room22019tuckedtstripes", "shirt-n_room22019overalltop", "shirt-n_room22019denimdress", "shirt-n_room22019bratoppink", "shirt-n_room12019sweaterwithbuttondowngrey", "shirt-n_room12019cropsweaterwhite", "shirt-n_room12019cropsweaterblack", "shirt-n_room12019buttondownblack", "shirt-n_philippineday2019filipinotop", "shirt-n_flashysuit", "shirt-n_SCSpring2018flowershirt", "shirt-n_2016fallblacklayeredbomber", "shirt-n_2016fallblackkknottedtee", "shirt-f_skullsweaterblack", "shirt-f_plaidtiedshirtred", "shirt-f_marchingband"]
                pant = ["shorts-f_pantyhoseshortsnavy", "pants-n_starteritems2019mensshortswhite", "pants-n_starteritems2019mensshortsblue", "pants-n_starteritems2019mensshortsblack", "pants-n_starteritems2019cuffedshortswhite", "pants-n_starteritems2019cuffedshortsblue", "pants-n_starteritems2019cuffedshortsblack", "pants-n_starteritems2019cuffedjeanswhite", "pants-n_starteritems2019cuffedjeansblue", "pants-n_starteritems2019cuffedjeansblack", "pants-n_room32019rippedpantswhite", "pants-n_room32019rippedpantsblue", "pants-n_room32019longtrackshortscamo", "pants-n_room32019longshortswithsocksgrey", "pants-n_room32019longshortswithsocksblack", "pants-n_room32019highwasittrackshortsblack", "pants-n_room32019baggytrackpantsred", "pants-n_room32019baggytrackpantsgreycamo", "pants-n_room22019undiespink", "pants-n_room22019undiesblack", "pants-n_room22019techpantscamo", "pants-n_room22019shortcutoffsdenim", "pants-n_room22019longcutoffsdenim", "pants-n_room12019rippedpantsblue", "pants-n_room12019rippedpantsblack", "pants-n_room12019formalslackskhaki", "pants-n_room12019formalslacksblack", "pants-n_room12019blackacidwashjeans", "pants-n_2016fallgreyacidwashjeans"]
                item_top = random.choice(shirt)
                item_bottom = random.choice(pant)
                xox = await self.highrise.set_outfit(outfit=[
                        Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=65),
                        Item(type='clothing', amount=1, id=item_top, account_bound=False, active_palette=-1),
                        Item(type='clothing', amount=1, id=item_bottom, account_bound=False, active_palette=-1),

                        Item(type='clothing', amount=1, id='nose-n_01', account_bound=False, active_palette=-1),
                        Item(type='clothing', amount=1, id='watch-n_room32019blackwatch', account_bound=False, active_palette=-1),
                        Item(type='clothing', amount=1, id='glasses-n_room12019circleframes', account_bound=False, active_palette=-1),
                        Item(type='clothing', amount=1, id='shoes-n_room12019sneakersblack', account_bound=False, active_palette=-1),
                        Item(type='clothing', amount=1, id='mouth-basic2018downturnedthinround', account_bound=False, active_palette=0),
                        Item(type='clothing', amount=1, id='hair_front-n_malenew07', account_bound=False, active_palette=1),
                        Item(type='clothing', amount=1, id='hair_back-n_malenew07', account_bound=False, active_palette=1),
                        Item(type='clothing', amount=1, id='bag-n_room12019backpack', account_bound=False, active_palette=-1),
                        Item(type='clothing', amount=1, id='eye-n_basic2018zanyeyes', account_bound=False, active_palette=-1),
                        Item(type='clothing', amount=1, id='eyebrow-n_basic2018newbrows09', account_bound=False, active_palette=-1)
                ])
                await self.highrise.chat(f"{xox}")
          
            if message.lower().strip() == "lambipose":
                await self.highrise.send_emote("emote-superpose", user.id)
            elif message.lower().strip() == "shuffledance":
                await self.highrise.send_emote("dance-tiktok10", user.id)
            elif message.lower().strip() == "gravedance":
                await self.highrise.send_emote("dance-weird", user.id)
            elif message.lower().strip() == "fighter":
                await self.highrise.send_emote("idle-fighter", user.id)
            elif message.lower().strip() == "renegade":
                await self.highrise.send_emote("idle-dance-tiktok7", user.id)
            elif message.lower().strip() == "singalong":
                await self.highrise.send_emote("idle_singing", user.id)
            elif message.lower().strip() == "froggiehop":
                await self.highrise.send_emote("emote-frog", user.id)
            elif message.lower().strip() == "viralgroove":
                await self.highrise.send_emote("dance-tiktok9", user.id)
            elif message.lower().strip() == "swordfight":
                await self.highrise.send_emote("emote-swordfight", user.id)
            elif message.lower().strip() == "energyball":
                await self.highrise.send_emote("emote-energyball", user.id)
            elif message.lower().strip() == "emotecute":
                await self.highrise.send_emote("emote-cute", user.id)
            elif message.lower().strip() == "floating":
                await self.highrise.send_emote("emote-float", user.id)
            elif message.lower().strip() == "teleport":
                await self.highrise.send_emote("emote-teleporting", user.id)
            elif message.lower().strip() == "telekinesis":
                await self.highrise.send_emote("emote-telekinesis", user.id)
            elif message.lower().strip() == "maniac":
                await self.highrise.send_emote("emote-maniac", user.id)
            elif message.lower().strip() == "embarrassed":
                await self.highrise.send_emote("emote-embarrassed", user.id)
            elif message.lower().strip() == "pissedoff":
                await self.highrise.send_emote("emote-frustrated", user.id)
            elif message.lower().strip() == "slap":
                await self.highrise.send_emote("emote-slap", user.id)
            elif message.lower().strip() == "dotheworm":
                await self.highrise.send_emote("emote-snake", user.id)
            elif message.lower().strip() == "enthused":
                await self.highrise.send_emote("idle-enthusiastic", user.id)
            elif message.lower().strip() == "confusion":
                await self.highrise.send_emote("emote-confused", user.id)
            elif message.lower().strip() == "shopping":
                await self.highrise.send_emote("dance-shoppingcart", user.id)
            elif message.lower().strip() == "roll":
                await self.highrise.send_emote("emote-roll", user.id)
            elif message.lower().strip() == "rofl":
                await self.highrise.send_emote("emote-rofl", user.id)
            elif message.lower().strip() == "superpunch":
                await self.highrise.send_emote("emote-superpunch", user.id)
            elif message.lower().strip() == "superrun":
                await self.highrise.send_emote("emote-superrun", user.id)
            elif message.lower().strip() == "superkick":
                await self.highrise.send_emote("emote-kicking", user.id)
            elif message.lower().strip() == "zombiedance":
                await self.highrise.send_emote("dance-zombie", user.id)
            elif message.lower().strip() == "monsterfail":
                await self.highrise.send_emote("emote-monster_fail", user.id)
            elif message.lower().strip() == "peekaboo":
                await self.highrise.send_emote("emote-peekaboo", user.id)
            elif message.lower().strip() == "sumofight":
                await self.highrise.send_emote("emote-sumo", user.id)
            elif message.lower().strip() == "charging":
                await self.highrise.send_emote("emote-charging", user.id)
            elif message.lower().strip() == "ninjarun":
                await self.highrise.send_emote("emote-ninjarun", user.id)
            elif message.lower().strip() == "proposing":
                await self.highrise.send_emote("emote-proposing", user.id)
            elif message.lower().strip() == "ropepull":
                await self.highrise.send_emote("emote-ropepull", user.id)
            elif message.lower().strip() == "secrethandshake":
                await self.highrise.send_emote("emote-secrethandshake", user.id)
            elif message.lower().strip() == "elbowbump":
                await self.highrise.send_emote("emote-elbowbump", user.id)
            elif message.lower().strip() == "homerun":
                await self.highrise.send_emote("emote-baseball", user.id)
            elif message.lower().strip() == "relaxing":
                await self.highrise.send_emote("idle-floorsleeping2", user.id)
            elif message.lower().strip() == "partnerhug":
                await self.highrise.send_emote("emote-hug", user.id)
            elif message.lower().strip() == "cozynap":
                await self.highrise.send_emote("idle-floorsleeping", user.id)
            elif message.lower().strip() == "hugyourself":
                await self.highrise.send_emote("emote-hugyourself", user.id)
            elif message.lower().strip() == "snowballfight":
                await self.highrise.send_emote("emote-snowball", user.id)
            elif message.lower().strip() == "sweating":
                await self.highrise.send_emote("emote-hot", user.id)
            elif message.lower().strip() == "levelup":
                await self.highrise.send_emote("emote-levelup", user.id)
            elif message.lower().strip() == "snowangel":
                await self.highrise.send_emote("emote-snowangel", user.id)
            elif message.lower().strip() == "posh":
                await self.highrise.send_emote("idle-posh", user.id)
            elif message.lower().strip() == "fallingapart":
                await self.highrise.send_emote("emote-apart", user.id)
            elif message.lower().strip() == "poutyface":
                await self.highrise.send_emote("idle-sad", user.id)
            elif message.lower().strip() == "Irritated":
                await self.highrise.send_emote("idle-angry", user.id)
            elif message.lower().strip() == "heroentrance":
                await self.highrise.send_emote("emote-hero", user.id)
            elif message.lower().strip() == "heropose":
                await self.highrise.send_emote("idle-hero", user.id)
            elif message.lower().strip() == "russiandance":
                await self.highrise.send_emote("dance-russian", user.id)
            elif message.lower().strip() == "curtsy":
                await self.highrise.send_emote("emote-curtsy", user.id)
            elif message.lower().strip() == "bow":
                await self.highrise.send_emote("emote-bow", user.id)
            elif message.lower().strip() == "ponder":
                await self.highrise.send_emote("idle-lookup", user.id)
            elif message.lower().strip() == "headball":
                await self.highrise.send_emote("emote-headball", user.id)
            elif message.lower().strip() == "clumsy":
                await self.highrise.send_emote("emote-fail2", user.id)
            elif message.lower().strip() == "fall":
                await self.highrise.send_emote("emote-fail1", user.id)
            elif message.lower().strip() == "penny":
                await self.highrise.send_emote("dance-pennywise", user.id)
            elif message.lower().strip() == "boo":
                await self.highrise.send_emote("emote-boo", user.id)
            elif message.lower().strip() == "fly":
                await self.highrise.send_emote("emote-wings", user.id)
            elif message.lower().strip() == "floss":
                await self.highrise.send_emote("dance-floss", user.id)
            elif message.lower().strip() == "kpop":
                await self.highrise.send_emote("dance-blackpink", user.id)
            elif message.lower().strip() == "model":
                await self.highrise.send_emote("emote-model", user.id)
            elif message.lower().strip() == "theatrical":
                await self.highrise.send_emote("emote-theatrical", user.id)
            elif message.lower().strip() == "amused":
                await self.highrise.send_emote("emote-laughing2", user.id)
            elif message.lower().strip() == "jetpack":
                await self.highrise.send_emote("emote-jetpack", user.id)
            elif message.lower().strip() == "bunnyhop":
                await self.highrise.send_emote("emote-bunnyhop", user.id)
            elif message.lower().strip() == "zombie":
                await self.highrise.send_emote("Idle_zombie", user.id)
            elif message.lower().strip() == "collapse":
                await self.highrise.send_emote("emote-death2", user.id)
            elif message.lower().strip() == "revival":
                await self.highrise.send_emote("emote-death", user.id)
            elif message.lower().strip() == "disco":
                await self.highrise.send_emote("emote-disco", user.id)
            elif message.lower().strip() == "relaxed":
                await self.highrise.send_emote("idle_layingdown2", user.id)
            elif message.lower().strip() == "attentive":
                await self.highrise.send_emote("idle_layingdown", user.id)
            elif message.lower().strip() == "faint":
                await self.highrise.send_emote("emote-faint", user.id)
            elif message.lower().strip() == "cold":
                await self.highrise.send_emote("emote-cold", user.id)
            elif message.lower().strip() == "sleepy":
                await self.highrise.send_emote("idle-sleep", user.id)
            elif message.lower().strip() == "handstand":
                await self.highrise.send_emote("emote-handstand", user.id)
            elif message.lower().strip() == "ghostfloat":
                await self.highrise.send_emote("emote-ghost-idle", user.id)
            elif message.lower().strip() == "ghost":
                await self.highrise.send_emote("emoji-ghost", user.id)
            elif message.lower().strip() == "splitsdrop":
                await self.highrise.send_emote("emote-splitsdrop", user.id)
            elif message.lower().strip() == "yogaflow":
                await self.highrise.send_emote("dance-spiritual", user.id)
            elif message.lower().strip() == "smoothwalk":
                await self.highrise.send_emote("dance-smoothwalk", user.id)
            elif message.lower().strip() == "ringonit":
                await self.highrise.send_emote("dance-singleladies", user.id)
            elif message.lower().strip() == "sick":
                await self.highrise.send_emote("emoji-sick", user.id)
            elif message.lower().strip() == "wiggledance":
                await self.highrise.send_emote("dance-sexy", user.id)
            elif message.lower().strip() == "robotic":
                await self.highrise.send_emote("dance-robotic", user.id)
            elif message.lower().strip() == "naughty":
                await self.highrise.send_emote("emoji-naughty", user.id)
            elif message.lower().strip() == "pray":
                await self.highrise.send_emote("emoji-pray", user.id)
            elif message.lower().strip() == "duckwalk":
                await self.highrise.send_emote("dance-duckwalk", user.id)
            elif message.lower().strip() == "faintdrop":
                await self.highrise.send_emote("emote-deathdrop", user.id)
            elif message.lower().strip() == "voguehands":
                await self.highrise.send_emote("dance-voguehands", user.id)
            elif message.lower().strip() == "orangejuicedance":
                await self.highrise.send_emote("dance-orangejustice", user.id)
            elif message.lower().strip() == "savagedance":
                await self.highrise.send_emote("dance-tiktok8", user.id)
            elif message.lower().strip() == "hearthands":
                await self.highrise.send_emote("emote-heartfingers", user.id)
            elif message.lower().strip() == "partnerheartarms":
                await self.highrise.send_emote("emote-heartshape", user.id)
            elif message.lower().strip() == "levitate":
                await self.highrise.send_emote("emoji-halo", user.id)
            elif message.lower().strip() == "sneeze":
                await self.highrise.send_emote("emoji-sneeze", user.id)
            elif message.lower().strip() == "donot":
                await self.highrise.send_emote("dance-tiktok2", user.id)
            elif message.lower().strip() == "rockout":
                await self.highrise.send_emote("dance-metal", user.id)
            elif message.lower().strip() == "pushups":
                await self.highrise.send_emote("dance-aerobics", user.id)
            elif message.lower().strip() == "karate":
                await self.highrise.send_emote("dance-martial-artist", user.id)
            elif message.lower().strip() == "macarena":
                await self.highrise.send_emote("dance-macarena", user.id)
            elif message.lower().strip() == "handsintheair":
                await self.highrise.send_emote("dance-handsup", user.id)
            elif message.lower().strip() == "breakdance":
                await self.highrise.send_emote("dance-breakdance", user.id)
            elif message.lower().strip() == "fireballlunge":
                await self.highrise.send_emote("emoji-hadoken", user.id)
            elif message.lower().strip() == "arrogance":
                await self.highrise.send_emote("emoji-arrogance", user.id)
            elif message.lower().strip() == "smirk":
                await self.highrise.send_emote("emoji-smirking", user.id)
            elif message.lower().strip() == "lying":
                await self.highrise.send_emote("emoji-lying", user.id)
            elif message.lower().strip() == "giveup":
                await self.highrise.send_emote("emoji-give-up", user.id)
            elif message.lower().strip() == "punch":
                await self.highrise.send_emote("emoji-punch", user.id)
            elif message.lower().strip() == "stinky":
                await self.highrise.send_emote("emoji-poop", user.id)
            elif message.lower().strip() == "point":
                await self.highrise.send_emote("emoji-there", user.id)
            elif message.lower().strip() == "annoyed":
                await self.highrise.send_emote("idle-loop-annoyed", user.id)
            elif message.lower().strip() == "taploop":
                await self.highrise.send_emote("idle-loop-tapdance", user.id)
            elif message.lower().strip() == "bummed":
                await self.highrise.send_emote("idle-loop-sad", user.id)
            elif message.lower().strip() == "chillin":
                await self.highrise.send_emote("idle-loop-happy", user.id)
            elif message.lower().strip() == "aerobics":
                await self.highrise.send_emote("idle-loop-aerobics", user.id)
            elif message.lower().strip() == "boogieswing":
                await self.highrise.send_emote("idle-dance-swinging", user.id)
            elif message.lower().strip() == "think":
                await self.highrise.send_emote("emote-think", user.id)
            elif message.lower().strip() == "blastoff":
                await self.highrise.send_emote("emote-disappear", user.id)
            elif message.lower().strip() == "gasp":
                await self.highrise.send_emote("emoji-scared", user.id)
            elif message.lower().strip() == "eyeroll":
                await self.highrise.send_emote("emoji-eyeroll", user.id)
            elif message.lower().strip() == "sob":
                await self.highrise.send_emote("emoji-crying", user.id)
            elif message.lower().strip() == "frolic":
                await self.highrise.send_emote("emote-frollicking", user.id)
            elif message.lower().strip() == "graceful":
                await self.highrise.send_emote("emote-graceful", user.id)
            elif message.lower().strip() == "rest":
                await self.highrise.send_emote("sit-idle-cute", user.id)
            elif message.lower().strip() == "greedyemote":
                await self.highrise.send_emote("emote-greedy", user.id)
            elif message.lower().strip() == "flirtywave":
                await self.highrise.send_emote("emote-lust", user.id)
            elif message.lower().strip() == "tiredx":
                await self.highrise.send_emote("idle-loop-tired", user.id)
            elif message.lower().strip() == "tummyache":
                await self.highrise.send_emote("emoji-gagging", user.id)
            elif message.lower().strip() == "flex":
                await self.highrise.send_emote("emoji-flex", user.id)
            elif message.lower().strip() == "raisetheroof":
                await self.highrise.send_emote("emoji-celebrate", user.id)
            elif message.lower().strip() == "cursingemote":
                await self.highrise.send_emote("emoji-cursing", user.id)
            elif message.lower().strip() == "stunned":
                await self.highrise.send_emote("emoji-dizzy", user.id)
            elif message.lower().strip() == "mindblown":
                await self.highrise.send_emote("emote-mindblown", user.id)
            elif message.lower().strip() == "shy":
                await self.highrise.send_emote("idle-loop-shy", user.id)
            elif message.lower().strip() == "sit":
                await self.highrise.send_emote("idle-loop-sitfloor", user.id)
            elif message.lower().strip() == "thumbsup":
                await self.highrise.send_emote("emote-thumbsup", user.id)
            elif message.lower().strip() == "clap":
                await self.highrise.send_emote("emote-clap", user.id)
            elif message.lower().strip() == "angry":
                await self.highrise.send_emote("emote-mad", user.id)
            elif message.lower().strip() == "tired":
                await self.highrise.send_emote("emote-sleepy", user.id)
            elif message.lower().strip() == "thewave":
                await self.highrise.send_emote("emote-thewave", user.id)
            elif message.lower().strip() == "thumbsuck":
                await self.highrise.send_emote("emote-suckthumb", user.id)
            elif message.lower().strip() == "shy":
                await self.highrise.send_emote("idle-loop-shy", user.id)
            elif message.lower().strip() == "peace":
                await self.highrise.send_emote("emote-peace", user.id)
            elif message.lower().strip() == "panic":
                await self.highrise.send_emote("emote-panic", user.id)
            elif message.lower().strip() == "jump":
                await self.highrise.send_emote("emote-jumpb", user.id)
            elif message.lower().strip() == "loveflutter":
                await self.highrise.send_emote("emote-hearteyes", user.id)
            elif message.lower().strip() == "exasperated":
                await self.highrise.send_emote("emote-exasperated", user.id)
            elif message.lower().strip() == "facepalm":
                await self.highrise.send_emote("emote-exasperatedb", user.id)
            elif message.lower().strip() == "dab":
                await self.highrise.send_emote("emote-dab", user.id)
            elif message.lower().strip() == "gangnamstyle":
                await self.highrise.send_emote("emote-gangnam", user.id)
            elif message.lower().strip() == "harlemshake":
                await self.highrise.send_emote("emote-harlemshake", user.id)
            elif message.lower().strip() == "tapdance":
                await self.highrise.send_emote("emote-tapdance", user.id)
            elif message.lower().strip() == "yes":
                await self.highrise.send_emote("emote-yes", user.id)
            elif message.lower().strip() == "sad":
                await self.highrise.send_emote("emote-sad", user.id)
            elif message.lower().strip() == "robot":
                await self.highrise.send_emote("emote-robot", user.id)
            elif message.lower().strip() == "rainbow":
                await self.highrise.send_emote("emote-rainbow", user.id)
            elif message.lower().strip() == "no":
                await self.highrise.send_emote("emote-no", user.id)
            elif message.lower().strip() == "nightfever":
                await self.highrise.send_emote("emote-nightfever", user.id)
            elif message.lower().strip() == "laugh":
                await self.highrise.send_emote("emote-laughing", user.id)
            elif message.lower().strip() == "kiss":
                await self.highrise.send_emote("emote-kiss", user.id)
            elif message.lower().strip() == "judochop":
                await self.highrise.send_emote("emote-judochop", user.id)
            elif message.lower().strip() == "hello":
                await self.highrise.send_emote("emote-hello", user.id)
            elif message.lower().strip() == "happy":
                await self.highrise.send_emote("emote-happy", user.id)
            elif message.lower().strip() == "moonwalk":
                await self.highrise.send_emote("emote-gordonshuffle", user.id)
            elif message.lower().strip() == "zombierun":
                await self.highrise.send_emote("emote-zombierun", user.id)
            elif message.lower().strip() == "cheerful":
                await self.highrise.send_emote("emote-pose8", user.id)
            elif message.lower().strip() == "embracingmodel":
                await self.highrise.send_emote("emote-pose7", user.id)
            elif message.lower().strip() == "embracing":
                await self.highrise.send_emote("emote-pose7", user.id)
            elif message.lower().strip() == "fashionpose":
                await self.highrise.send_emote("emote-pose5", user.id)
            elif message.lower().strip() == "fashion":
                await self.highrise.send_emote("emote-pose5", user.id)
            elif message.lower().strip() == "ichallengeyou":
                await self.highrise.send_emote("emote-pose3", user.id)
            elif message.lower().strip() == "challenge":
                await self.highrise.send_emote("emote-pose3", user.id)
            elif message.lower().strip() == "flirtywink":
                await self.highrise.send_emote("emote-pose1", user.id)
            elif message.lower().strip() == "wink":
                await self.highrise.send_emote("emote-pose1", user.id)
            elif message.lower().strip() == "acasualdance":
                await self.highrise.send_emote("idle-dance-casual", user.id)
            elif message.lower().strip() == "casualdance":
                await self.highrise.send_emote("idle-dance-casual", user.id)
            elif message.lower().strip() == "casual":
                await self.highrise.send_emote("idle-dance-casual", user.id)
            elif message.lower().strip() == "cutie":
                await self.highrise.send_emote("emote-cutey", user.id)
            elif message.lower().strip() == "zerogravity":
                await self.highrise.send_emote("emote-astronaut", user.id)
            elif message.lower().strip() == "zerogravity":
                await self.highrise.send_emote("emote-astronaut", user.id)
            elif message.lower().strip() == "saysodance":
                await self.highrise.send_emote("idle-dance-tiktok4", user.id)
            elif message.lower().strip() == "sodance":
                await self.highrise.send_emote("idle-dance-tiktok4", user.id)
            elif message.lower().strip() == "saydance":
                await self.highrise.send_emote("idle-dance-tiktok4", user.id)
            elif message.lower().strip() == "sayso":
                await self.highrise.send_emote("idle-dance-tiktok4", user.id)
            elif message.lower().strip() == "punkguitar":
                await self.highrise.send_emote("emote-punkguitar", user.id)
            elif message.lower().strip() == "punk":
                await self.highrise.send_emote("emote-punkguitar", user.id)
            elif message.lower().strip() == "guitar":
                 await self.highrise.send_emote("emote-punkguitar", user.id)
            elif message.lower().strip() == "icecream":
                await self.highrise.send_emote("dance-icecream", user.id)
            elif message.lower().strip() == "gravity":
                await self.highrise.send_emote("emote-gravity", user.id)
            elif message.lower().strip() == "fashionista":
                await self.highrise.send_emote("emote-fashionista", user.id)
            elif message.lower().strip() == "uwu":
                await self.highrise.send_emote("idle-uwu", user.id)
            elif message.lower().strip() == "uwumood":
                await self.highrise.send_emote("idle-uwu", user.id)
            elif message.lower().strip() == "wrong":
                await self.highrise.send_emote("dance-wrong", user.id)
            elif message.lower().strip() == "dancewrong":
                await self.highrise.send_emote("dance-wrong", user.id)
        except Exception as e:
            print(f"Error : {e}")
          
    async def run(self, room_id, token):
        definitions = [BotDefinition(self, room_id, token)]
        await __main__.main(definitions)

keep_alive()
if __name__ == "__main__":
    room_id ="65c7f3fc076d343df5935341" 
    token = "b825d5b1e00ba7e5289f9cc439f8d24fb6016da588f3338007ade5298db014b8"
    arun(Bot().run(room_id, token))
  