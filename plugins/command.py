import datetime
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import *
from pyrogram.errors import *
from Script import script
from database.users_db import db
from info import START_PIC, LOG_CHANNEL, PREMIUM_LOGS, FSUB, QR_CODE_IMAGE, DAILY_LIMIT, PREMIUM_DAILY_LIMIT, UPI_ID
from utils import temp, is_user_joined
from plugins.verification import verify_user_on_start
from plugins.send_file import send_requested_file
from plugins.refer import refer_on_start

# =================================================
# 🚀 START COMMAND
# =================================================
@Client.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    user_id = message.from_user.id
    mention = message.from_user.mention
    me2 = (await client.get_me()).mention
    
    if FSUB and not await is_user_joined(client, message):
        return
        
    argument = message.command[1] if len(message.command) > 1 else None

    if argument and argument.startswith('avbotz'):
        await verify_user_on_start(client, message)
        return

    if argument == "terms":
        await send_legal_text(client, message, script.TERMS_TXT)
        return
    elif argument == "disclaimer":
        await send_legal_text(client, message, script.DISCLAIMER_TXT)
        return
    elif argument == "help":
        await send_legal_text(client, message, script.HELP_TXT)
        return
    elif argument == "about":
        await send_about_text(client, message)
        return

    if argument and argument.startswith("reff_"):
        try:
            await refer_on_start(client, message)
            return 
        except Exception as e:
            print(f"Referral Error: {e}")

    if argument and argument.startswith("avx-"):
        search_id = argument.replace("avx-", "")
        await send_requested_file(client, message, user_id, search_id)
        return

    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, message.from_user.first_name)
        try:
            await client.send_message(
                LOG_CHANNEL,
                script.LOG_TEXT.format(me2, user_id, mention)
            )
        except Exception:
            pass
            
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("Get Video"), KeyboardButton("Brazzers")],
            [KeyboardButton("My plan"), KeyboardButton("Subscription")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

    await message.reply_photo(
        photo=START_PIC,
        caption=script.START_TXT.format(mention, temp.U_NAME, temp.U_NAME),
        reply_markup=reply_keyboard,
        has_spoiler=True
    )

# =================================================
# 📜 HELPER HANDLERS
# =================================================

@Client.on_message(filters.command("disclaimer") & filters.private)
async def legal_disclaimer(client, message: Message):
    await send_legal_text(client, message, script.DISCLAIMER_TXT)

@Client.on_message(filters.command("terms") & filters.private)
async def legal_terms(client, message: Message):
    await send_legal_text(client, message, script.TERMS_TXT)

@Client.on_message(filters.command("about") & filters.private)
async def legal_about(client, message: Message):
    await send_about_text(client, message)

@Client.on_message(filters.command("help") & filters.private)
async def legal_hepl(client, message: Message):
    await send_legal_text(client, message, script.HELP_TXT)
    
async def send_legal_text(client, message, text):
    inline_buttons = [[
        InlineKeyboardButton('• ᴄʟᴏsᴇ •', callback_data='close_data')
    ]]
    await message.reply_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_buttons),
        disable_web_page_preview=True
    )

async def send_about_text(client, message):
    inline_buttons = [[
        InlineKeyboardButton('• ᴄʟᴏsᴇ •', callback_data='close_data')
    ]]
    await message.reply_text(
        text=script.ABOUT_TXT.format(temp.B_NAME, temp.B_LINK),
        reply_markup=InlineKeyboardMarkup(inline_buttons),
        disable_web_page_preview=True
    )

# =========================================================
# 🔙 CALLBACK QUERY HANDLER
# =========================================================

from os import environ
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, InputMediaVideo
from database.users_db import db
from info import PROTECT_CONTENT, DAILY_LIMIT, PREMIUM_DAILY_LIMIT, VERIFICATION_DAILY_LIMIT, FSUB, IS_VERIFY
import asyncio
from plugins.verification import av_x_verification
from plugins.ban_manager import ban_manager
from utils import temp, auto_delete_message, is_user_joined

user_last_video = {}

@Client.on_message(filters.command("getvideo") | filters.regex(r"(?i)get video"))
async def handle_video_request(client, m: Message):
    if not m.from_user:
        return

    await m.delete()

    if FSUB and not await is_user_joined(client, m):
        return

    user_id = m.from_user.id
    username = m.from_user.username or m.from_user.first_name or "Unknown"

    if await ban_manager.check_ban(client, m):
        return

    is_premium = await db.has_premium_access(user_id)
    used = await db.get_video_count(user_id) or 0

    limit_reached_msg = (
        f"𝖸𝗈𝗎'𝗏𝖾 𝖱𝖾𝖺𝖼𝗁𝖾𝖽 𝖸𝗈𝗎𝗋 𝖣𝖺𝗂𝗅𝗒 𝖫𝗂𝗆𝗂𝗍 𝖮𝖿 {used} 𝖥𝗂𝗅𝖾𝗌.\n\n"
        "𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇 𝖳𝗈𝗆𝗈𝗋𝗋𝗈𝗐!\n"
        "𝖮𝗋 𝖯𝗎𝗋𝖼𝗁𝖺𝗌𝖾 𝖲𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 𝖳𝗈 𝖡𝗈𝗈𝗌𝗍 𝖸𝗈𝗎𝗋 𝖣𝖺𝗂𝗅𝗒 𝖫𝗂𝗆𝗂𝗍"
    )
    buy_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("• 𝖯𝗎𝗋𝖼𝗁𝖺𝗌𝖾 𝖲𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 •", callback_data="get")]
    ])

    if is_premium:
        if used >= PREMIUM_DAILY_LIMIT:
            await m.reply(
                f"𝖸𝗈𝗎'𝗏𝖾 𝖱𝖾𝖺𝖼𝗁𝖾𝖽 𝖸𝗈𝗎𝗋 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖫𝗂𝗆𝗂𝗍 𝖮𝖿 {PREMIUM_DAILY_LIMIT} 𝖥𝗂𝗅𝖾𝗌.\n"
                f"𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇 𝖳𝗈𝗆𝗈𝗋𝗋𝗈𝗐!"
            )
            return
    else:
        if used >= VERIFICATION_DAILY_LIMIT:
            await m.reply(limit_reached_msg, reply_markup=buy_button)
            return
        if used >= DAILY_LIMIT:
            if IS_VERIFY:
                verified = await av_x_verification(client, m)
                if not verified:
                    return
            else:
                await m.reply(limit_reached_msg, reply_markup=buy_button)
                return

    video_id = await db.get_unseen_video(user_id)
    if not video_id:
        try:
            video_id = await db.get_random_video()
        except Exception as e:
            print(f"[Random Video Error] {e}")
            return

    if not video_id:
        await m.reply("❌ No videos found in the database.")
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⏩ Next", callback_data="nextv")]
    ])

    caption_text = (
        f"𝘗𝘰𝘸𝘦𝘳𝘦𝘥 𝘉𝘺: {temp.B_LINK}\n\n"
        "<blockquote>"
        "ᴛʜɪꜱ ꜰɪʟᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀꜰᴛᴇʀ 10 ᴍɪɴᴜᴛᴇꜱ.\n"
        "ᴘʟᴇᴀꜱᴇ ꜰᴏʀᴡᴀʀᴅ ᴛʜɪꜱ ꜰɪʟᴇ ꜱᴏᴍᴇᴡʜᴇʀᴇ ᴇʟꜱᴇ "
        "ᴏʀ ꜱᴀᴠᴇ ɪɴ ꜱᴀᴠᴇᴅ ᴍᴇꜱꜱᴀɢᴇꜱ."
        "</blockquote>"
    )

    # ----- FIX: handle stale message gracefully -----
    try:
        last_msg = user_last_video.get(user_id)
        if last_msg and isinstance(last_msg, dict):
            chat_id = last_msg.get("chat_id")
            message_id = last_msg.get("message_id")
            if chat_id and message_id:
                try:
                    media = InputMediaVideo(media=video_id, caption=caption_text)
                    await client.edit_message_media(
                        chat_id=chat_id,
                        message_id=message_id,
                        media=media,
                        reply_markup=keyboard
                    )
                    sent = last_msg
                    sent["video_id"] = video_id
                    return  # edit succeeded, we're done
                except Exception as edit_err:
                    # Message is gone (invalid id) – fall through to send new
                    if "MESSAGE_ID_INVALID" not in str(edit_err) and "message id is invalid" not in str(edit_err).lower():
                        raise  # unexpected error
                    user_last_video.pop(user_id, None)  # remove stale entry
    except Exception:
        pass  # fall back to sending new message

    # Send a new video
    sent = await client.send_video(
        chat_id=m.chat.id,
        video=video_id,
        protect_content=PROTECT_CONTENT,
        caption=caption_text,
        reply_markup=keyboard,
        reply_to_message_id=None
    )
    user_last_video[user_id] = {
        "chat_id": sent.chat.id,
        "message_id": sent.id,
        "video_id": video_id
    }
    asyncio.create_task(auto_delete_message(m, sent))
    await db.increase_video_count(user_id, username)

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id

    if data == "close_data":
        await query.message.delete()

    elif data == "get":
        buttons = [
            [InlineKeyboardButton('• 𝖢𝗅𝗈𝗌𝖾 •', callback_data='close_data')]
        ]
        await query.message.reply_photo(
            photo=QR_CODE_IMAGE,
            caption=script.SEENBUY_TXT.format(DAILY_LIMIT, PREMIUM_DAILY_LIMIT, UPI_ID),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )

    elif data == "nextv":
        username = query.from_user.username or query.from_user.first_name or "Unknown"

        if await ban_manager.check_ban(client, query.message):
            await query.answer("You are banned.", show_alert=True)
            return

        is_premium = await db.has_premium_access(user_id)
        used = await db.get_video_count(user_id) or 0

        if is_premium:
            if used >= PREMIUM_DAILY_LIMIT:
                await query.answer(f"Daily premium limit ({PREMIUM_DAILY_LIMIT}) reached.", show_alert=True)
                return
        else:
            if used >= VERIFICATION_DAILY_LIMIT:
                await query.answer("Daily limit reached. Upgrade to premium.", show_alert=True)
                return
            if used >= DAILY_LIMIT:
                if IS_VERIFY:
                    verified = await av_x_verification(client, query.message)
                    if not verified:
                        await query.answer("Verification required.", show_alert=True)
                        return
                else:
                    await query.answer(f"Daily limit ({DAILY_LIMIT}) reached.", show_alert=True)
                    return

        video_id = await db.get_unseen_video(user_id)
        if not video_id:
            try:
                video_id = await db.get_random_video()
            except Exception as e:
                print(f"[Random Video Error] {e}")
                await query.answer("No videos available.", show_alert=True)
                return

        if not video_id:
            await query.answer("No videos found.", show_alert=True)
            return

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⏩ Next", callback_data="nextv")]
        ])
        caption_text = (
            f"𝘗𝘰𝘸𝘦𝘳𝘦𝘥 𝘉𝘺: {temp.B_LINK}\n\n"
            "<blockquote>"
            "ᴛʜɪꜱ ꜰɪʟᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀꜰᴛᴇʀ 10 ᴍɪɴᴜᴛᴇꜱ.\n"
            "ᴘʟᴇᴀꜱᴇ ꜰᴏʀᴡᴀʀᴅ ᴛʜɪꜱ ꜰɪʟᴇ ꜱᴏᴍᴇᴡʜᴇʀᴇ ᴇʟꜱᴇ "
            "ᴏʀ ꜱᴀᴠᴇ ɪɴ ꜱᴀᴠᴇᴅ ᴍᴇꜱꜱᴀɢᴇꜱ."
            "</blockquote>"
        )

        # ----- FIX: handle stale message gracefully -----
        try:
            media = InputMediaVideo(media=video_id, caption=caption_text)
            await client.edit_message_media(
                chat_id=query.message.chat.id,
                message_id=query.message.id,
                media=media,
                reply_markup=keyboard
            )
            await db.increase_video_count(user_id, username)
            await query.answer("New video loaded!")
        except Exception as edit_err:
            if "MESSAGE_ID_INVALID" in str(edit_err) or "message id is invalid" in str(edit_err).lower():
                # Original message is gone – send a fresh video
                try:
                    await query.message.delete()
                except:
                    pass
                sent = await client.send_video(
                    chat_id=query.message.chat.id,
                    video=video_id,
                    protect_content=PROTECT_CONTENT,
                    caption=caption_text,
                    reply_markup=keyboard
                )
                # Update stored reference
                user_last_video[user_id] = {
                    "chat_id": sent.chat.id,
                    "message_id": sent.id,
                    "video_id": video_id
                }
                await db.increase_video_count(user_id, username)
                await query.answer("New video sent (previous message was unavailable).", show_alert=False)
            else:
                await query.answer(f"Error: {str(edit_err)}", show_alert=True)