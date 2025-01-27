import os
import json
from dotenv import load_dotenv, set_key, unset_key
from pyrogram import Client, filters
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message

# Importing from data.py which imports XoGameObject.py and emojis.py
from data import *  # This will import the necessary game data and logic from data.py

# Load environment variables from .env file
load_dotenv()

# Function to set environment variables (to update .env file)
def set_env_var(key, value):
    set_key(".env", key, value)

# Function to remove environment variables (to clean up .env file)
def remove_env_var(key):
    unset_key(".env", key)

# Initialize the client app using the environment variables
app = Client(
    "XOGame",  # This will automatically create a session file with this name
    api_id=os.environ.get("API_ID"),
    api_hash=os.environ.get("API_HASH"),
    bot_token=os.environ.get("BOT_TOKEN")
)

def mention(name: str, id: int) -> str:
    return "[{}](tg://user?id={})".format(name, id)

# Define InlineKeyboardMarkup for support and developer contact
CONTACT_KEYS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            emojis.cat + " Sᴜᴘᴘᴏʀᴛ",  # Support button
            url="https://telegram.me/storm_techh"
        ),
        InlineKeyboardButton(
            emojis.id + " Dᴇᴠᴇʟᴏᴘᴇʀ",  # Developer button
            url="http://telegram.me/interstellarXd"
        )
    ],
    [
        InlineKeyboardButton(
            emojis.mail + " email",  # Chat button
            json.dumps({
                "type": "C",
                "action": "email"
            })
        )
    ]
])

@app.on_message(filters.private & filters.text)
async def message_handler(bot: Client, message: Message):
    if message.text == "/start":
        await bot.send_message(
            message.from_user.id,
            f"ʜɪ **{message.from_user.first_name}**\n\nTᴏ Sᴛᴀʀᴛ Pʟᴀʏɪɴɢ  Bɪʟʟᴀ XO Gᴀᴍᴇ , Sᴛᴀʀᴛ Mᴇ Fɪʀsᴛ Iɴ Pᴍ"
            "Aᴅᴅ @BillaXoBot ɪɴ ᴀɴʏ ᴄʜᴀᴛ ʏᴏᴜ ᴡᴀɴᴛ ᴏʀ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ **Pʟᴀʏ** ʙᴜᴛᴛᴏɴ "
            "Aɴᴅ Sᴇʟᴇᴄᴛ A Cʜᴀᴛ Tᴏ Pʟᴀʏ Iɴ.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    emojis.game + " Play",  # Play button
                    switch_inline_query=emojis.game
                )]
            ])
        )
    elif message.text == "/inquiry":
        await bot.send_message(
            message.from_user.id,
            "Fᴇᴇʟ Fʀᴇᴇ Tᴏ Sʜᴀʀᴇ Yᴏᴜʀ Tʜᴏᴜɢʜᴛs Oɴ Bɪʟʟᴀ Xᴏ Bᴏᴛ Wɪᴛʜ Mᴇ.",
            reply_markup=CONTACT_KEYS
        )


@app.on_inline_query()
async def inline_query_handler(_, query: InlineQuery):
    await query.answer(
        results=[InlineQueryResultArticle(
            title="Tɪᴄ-Tᴀᴄ-Tᴏᴇ",
            input_message_content=InputTextMessageContent(
                f"**{query.from_user.first_name}** Cʜᴀʟʟᴇɴɢᴇᴅ Yᴏᴜ Iɴ Xo!"
            ),
            description="Tᴀᴘ ʜᴇʀᴇ ᴛᴏ ᴄʜᴀʟʟᴇɴɢᴇ ʏᴏᴜʀ ғʀɪᴇɴᴅs ɪɴ XO!",
            thumb_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Tic_tac_toe.svg/1200px-Tic_tac_toe"
                      ".svg.png",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(
                    emojis.swords + " Aᴄᴄᴇᴘᴛ",  # Accept button
                    json.dumps(
                        {"type": "P",
                         "id": query.from_user.id,
                         "name": query.from_user.first_name
                         }
                    )
                )]]
            )
        )],
        cache_time=1
    )


@app.on_callback_query()
async def callback_query_handler(bot: Client, query: CallbackQuery):
    data = json.loads(query.data)
    game = get_game(query.inline_message_id, data)
    if data["type"] == "P":  # Player
        if game.player1["id"] == query.from_user.id:
            await bot.answer_callback_query(
                query.id,
                "Wᴀɪᴛ ғᴏʀ ᴏᴘᴘᴏɴᴇɴᴛ!",
                show_alert=True
            )
        elif game.player1["id"] != query.from_user.id:
            game.player2 = {"type": "P",
                            "id": query.from_user.id,
                            "name": query.from_user.first_name
                            }

            message_text = "{}({})  {}  {}({})\n\n{} **{} ({})**".format(
                mention(game.player1["name"], game.player1["id"]),
                emojis.X,  # X emoji
                emojis.vs,  # VS emoji
                mention(game.player2["name"], game.player2["id"]),
                emojis.O,  # O emoji
                emojis.game,
                mention(game.player1["name"], game.player1["id"]),
                emojis.X  # X emoji
            )

            await bot.edit_inline_text(
                query.inline_message_id,
                message_text,
                reply_markup=InlineKeyboardMarkup(game.board_keys)
            )
    elif data["type"] == "K":  # Keyboard
        if data["end"]:
            await bot.answer_callback_query(
                query.id,
                "Mᴀᴛᴄʜ ʜᴀs ᴇɴᴅᴇᴅ!",
                show_alert=True
            )

            return

        if (game.whose_turn and query.from_user.id != game.player1["id"]) \
                or (not game.whose_turn and query.from_user.id != game.player2["id"]):
            await bot.answer_callback_query(
                query.id,
                "Nᴏᴛ ʏᴏᴜʀ ᴛᴜʀɴ!"
            )

            return

        if game.fill_board(query.from_user.id, data["coord"]):
            game.whose_turn = not game.whose_turn

            if game.check_winner():
                message_text = "{}({})  {}  {}({})\n\n{} **{} won!**".format(
                    mention(game.player1["name"], game.player1["id"]),
                    emojis.X,  # X emoji
                    emojis.vs,  # VS emoji
                    mention(game.player2["name"], game.player2["id"]),
                    emojis.O,  # O emoji
                    emojis.trophy,  # Trophy emoji
                    mention(game.winner["name"], game.winner["id"])
                )
            elif game.is_draw():
                message_text = "{}({})  {}  {}({})\n\n{} **Draw!**".format(
                    mention(game.player1["name"], game.player1["id"]),
                    emojis.X,  # X emoji
                    emojis.vs,  # VS emoji
                    mention(game.player2["name"], game.player2["id"]),
                    emojis.O,  # O emoji
                    emojis.draw  # Draw emoji
                )
            else:
                message_text = "{}({})  {}  {}({})\n\n{} **{} ({})**".format(
                    mention(game.player1["name"], game.player1["id"]),
                    emojis.X,  # X emoji
                    emojis.vs,  # VS emoji
                    mention(game.player2["name"], game.player2["id"]),
                    emojis.O,  # O emoji
                    emojis.game,
                    mention(game.player1["name"], game.player1["id"]) if game.whose_turn else
                    mention(game.player2["name"], game.player2["id"]),
                    emojis.X if game.whose_turn else emojis.O
                )

            await bot.edit_inline_text(
                query.inline_message_id,
                message_text,
                reply_markup=InlineKeyboardMarkup(game.board_keys)
            )
        else:
            await bot.answer_callback_query(
                query.id,
                "Tʜɪs ᴏɴᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴛᴀᴋᴇɴ!"
            )
    elif data["type"] == "R":  # Reset
        game = reset_game(game)

        message_text = "{}({})  {}  {}({})\n\n{} **{} ({})**".format(
            mention(game.player1["name"], game.player1["id"]),
            emojis.X,  # X emoji
            emojis.vs,  # VS emoji
            mention(game.player2["name"], game.player2["id"]),
            emojis.O,  # O emoji
            emojis.game,
            mention(game.player1["name"], game.player1["id"]),
            emojis.X  # X emoji
        )

        await bot.edit_inline_text(
            query.inline_message_id,
            message_text,
            reply_markup=InlineKeyboardMarkup(game.board_keys)
        )
    elif data["type"] == "C":  # Contact
        if data["action"] == "Cʜᴀᴛ":
            await bot.edit_message_text(
                query.from_user.id,
                query.message.message_id,
                "StormVortexv2@gmail.com",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(
                        emojis.back + " back",  # Back button
                        json.dumps(
                            {"type": "C",
                             "action": "email-back"
                             }
                        )
                    )]]
                )
            )
        elif data["action"] == "email-back":
            await bot.edit_message_text(
                query.from_user.id,
                query.message.message_id,
                "Fᴇᴇʟ Fʀᴇᴇ Tᴏ Sʜᴀʀᴇ Yᴏᴜʀ Tʜᴏᴜɢʜᴛs Oɴ Bɪʟʟᴀ Xᴏ Hᴇʀᴇ @BillaCore.",
                reply_markup=CONTACT_KEYS
            )


app.run()
