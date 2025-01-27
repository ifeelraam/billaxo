import os

from data import *
from pyrogram import Client, filters
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, \
    InlineKeyboardMarkup, CallbackQuery, Message


app = Client(session_name="XOGame",
             api_id=os.environ.get("API_ID"),
             api_hash=os.environ.get("API_HASH"),
             bot_token=os.environ.get("BOT_TOKEN")
             )


def mention(name: str, id: int) -> str:
    return "[{}](tg://user?id={})".format(name, id)


CONTACT_KEYS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            emojis.cat + " Sᴜᴘᴘᴏʀᴛ",
            url="https://telegram.me/storm_techh"
        ),
        InlineKeyboardButton(
            emojis.id + " Dᴇᴠᴇʟᴏᴘᴇʀ",
            url="http://telegram.me/interstellarXd"
        )
    ],
    [
        InlineKeyboardButton(
            emojis.mail + " Cʜᴀᴛ",
            json.dumps({
                "type": "C",
                "action": "Cʜᴀᴛ"
            })
        )
    ]
])


@app.on_message(filters.private & filters.text)
def message_handler(bot: Client, message: Message):
    if message.text == "/start":
        bot.send_message(
            message.from_user.id,
            f"ʜɪ **{message.from_user.first_name}**\n\nTᴏ Sᴛᴀʀᴛ Pʟᴀʏɪɴɢ  Bɪʟʟᴀ XO Gᴀᴍᴇ , Sᴛᴀʀᴛ Mᴇ Fɪʀsᴛ Iɴ Pᴍ"
            "Aᴅᴅ @BillaXoBot ɪɴ ᴀɴʏ ᴄʜᴀᴛ ʏᴏᴜ ᴡᴀɴᴛ ᴏʀ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ **Pʟᴀʏ** ʙᴜᴛᴛᴏɴ "
            "Aɴᴅ Sᴇʟᴇᴄᴛ A Cʜᴀᴛ Tᴏ Pʟᴀʏ Iɴ.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    emojis.game + " Play",
                    switch_inline_query=emojis.game
                )]
            ])
        )
    elif message.text == "/inquiry":
        bot.send_message(
            message.from_user.id,
            "Fᴇᴇʟ Fʀᴇᴇ Tᴏ Sʜᴀʀᴇ Yᴏᴜʀ Tʜᴏᴜɢʜᴛs Oɴ Bɪʟʟᴀ Xᴏ Bᴏᴛ Wɪᴛʜ Mᴇ.",
            reply_markup=CONTACT_KEYS
        )


@app.on_inline_query()
def inline_query_handler(_, query: InlineQuery):
    query.answer(
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
                    emojis.swords + " Aᴄᴄᴇᴘᴛ",
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
def callback_query_handler(bot: Client, query: CallbackQuery):
    data = json.loads(query.data)
    game = get_game(query.inline_message_id, data)
    if data["type"] == "P":  # Player
        if game.player1["id"] == query.from_user.id:
            bot.answer_callback_query(
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
                emojis.X,
                emojis.vs,
                mention(game.player2["name"], game.player2["id"]),
                emojis.O,
                emojis.game,
                mention(game.player1["name"], game.player1["id"]),
                emojis.X
            )

            bot.edit_inline_text(
                query.inline_message_id,
                message_text,
                reply_markup=InlineKeyboardMarkup(game.board_keys)
            )
    elif data["type"] == "K":  # Keyboard
        if data["end"]:
            bot.answer_callback_query(
                query.id,
                "Mᴀᴛᴄʜ ʜᴀs ᴇɴᴅᴇᴅ!",
                show_alert=True
            )

            return

        if (game.whose_turn and query.from_user.id != game.player1["id"]) \
                or (not game.whose_turn and query.from_user.id != game.player2["id"]):
            bot.answer_callback_query(
                query.id,
                "Nᴏᴛ ʏᴏᴜʀ ᴛᴜʀɴ!"
            )

            return

        if game.fill_board(query.from_user.id, data["coord"]):
            game.whose_turn = not game.whose_turn

            if game.check_winner():
                message_text = "{}({})  {}  {}({})\n\n{} **{} won!**".format(
                    mention(game.player1["name"], game.player1["id"]),
                    emojis.X,
                    emojis.vs,
                    mention(game.player2["name"], game.player2["id"]),
                    emojis.O,
                    emojis.trophy,
                    mention(game.winner["name"], game.winner["id"])
                )
            elif game.is_draw():
                message_text = "{}({})  {}  {}({})\n\n{} **Draw!**".format(
                    mention(game.player1["name"], game.player1["id"]),
                    emojis.X,
                    emojis.vs,
                    mention(game.player2["name"], game.player2["id"]),
                    emojis.O,
                    emojis.draw
                )
            else:
                message_text = "{}({})  {}  {}({})\n\n{} **{} ({})**".format(
                    mention(game.player1["name"], game.player1["id"]),
                    emojis.X,
                    emojis.vs,
                    mention(game.player2["name"], game.player2["id"]),
                    emojis.O,
                    emojis.game,
                    mention(game.player1["name"], game.player1["id"]) if game.whose_turn else
                    mention(game.player2["name"], game.player2["id"]),
                    emojis.X if game.whose_turn else emojis.O
                )

            bot.edit_inline_text(
                query.inline_message_id,
                message_text,
                reply_markup=InlineKeyboardMarkup(game.board_keys)
            )
        else:
            bot.answer_callback_query(
                query.id,
                "Tʜɪs ᴏɴᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴛᴀᴋᴇɴ!"
            )
    elif data["type"] == "R":  # Reset
        game = reset_game(game)

        message_text = "{}({})  {}  {}({})\n\n{} **{} ({})**".format(
            mention(game.player1["name"], game.player1["id"]),
            emojis.X,
            emojis.vs,
            mention(game.player2["name"], game.player2["id"]),
            emojis.O,
            emojis.game,
            mention(game.player1["name"], game.player1["id"]),
            emojis.X
        )

        bot.edit_inline_text(
            query.inline_message_id,
            message_text,
            reply_markup=InlineKeyboardMarkup(game.board_keys)
        )
    elif data["type"] == "C":  # Contact
        if data["action"] == "Cʜᴀᴛ":
            bot.edit_message_text(
                query.from_user.id,
                query.message.message_id,
                "https://t.me/Harmony_Hub8",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(
                        emojis.back + " Bᴀᴄᴋ",
                        json.dumps(
                            {"type": "C",
                             "action": "Cʜᴀᴛ-Bᴀᴄᴋ"
                             }
                        )
                    )]]
                )
            )
        elif data["action"] == "email-back":
            bot.edit_message_text(
                query.from_user.id,
                query.message.message_id,
                "Fᴇᴇʟ Fʀᴇᴇ Tᴏ Sʜᴀʀᴇ Yᴏᴜʀ Tʜᴏᴜɢʜᴛs Oɴ Bɪʟʟᴀ Xᴏ Hᴇʀᴇ @BillaCore.",
                reply_markup=CONTACT_KEYS
            )


app.run()
