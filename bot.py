import os
import re
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_CHAT_ID = int(os.environ["ADMIN_CHAT_ID"])

PAID_LINK = "https://t.me/+CzC7KBjLbDhkNDlk"

PORT = int(os.environ.get("PORT", "10000"))
HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if not HOSTNAME:
    raise RuntimeError("RENDER_EXTERNAL_HOSTNAME is not available")

WEBHOOK_URL = f"https://{HOSTNAME}/telegram"


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ Subscribe — $40/month", url=PAID_LINK)],
        [
            InlineKeyboardButton("📊 What You Get", callback_data="what"),
            InlineKeyboardButton("💳 Plans", callback_data="plans"),
        ],
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
            InlineKeyboardButton("❓ FAQ", callback_data="faq"),
        ],
        [InlineKeyboardButton("🆘 Support", callback_data="support")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("support_mode", None)

    await update.message.reply_text(
        "Welcome to 2WAYARB — Relative Value Signals.\n\n"
        "Real-time spread-arbitrage signals focused primarily "
        "on major indices, with selected FX opportunities.\n\n"
        "No courses. No hype. Just the trades.\n\n"
        "Choose an option below:",
        reply_markup=main_menu(),
    )


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("support_mode", None)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ Subscribe Now", url=PAID_LINK)],
        [InlineKeyboardButton("⬅️ Back", callback_data="home")],
    ])

    await update.message.reply_text(
        "⭐ 2WAYARB Monthly Access\n\n"
        "Subscription: $40/month\n\n"
        "Tap below to subscribe and receive access "
        "to the private 2WAYARB channel.",
        reply_markup=keyboard,
    )


async def plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await subscribe(update, context)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("support_mode", None)

    await update.message.reply_text(
        "ℹ️ ABOUT 2WAYARB\n\n"
        "2WAYARB focuses on relative-value and "
        "spread-arbitrage opportunities, primarily "
        "across major indices and occasionally FX pairs.\n\n"
        "No training. No hype. Just signals."
    )


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("support_mode", None)

    await update.message.reply_text(
        "❓ FAQ\n\n"
        "Q: How much is access?\n"
        "A: $40/month.\n\n"
        "Q: How do I subscribe?\n"
        "A: Tap Subscribe and complete the Telegram payment.\n\n"
        "Q: Where are the signals delivered?\n"
        "A: Inside the private 2WAYARB Telegram channel.\n\n"
        "Q: Are profits guaranteed?\n"
        "A: No. Trading involves risk and past performance "
        "does not guarantee future results."
    )


async def support_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["support_mode"] = True

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="home")]
    ])

    message = (
        "🆘 SUPPORT\n\n"
        "Please describe your issue below.\n\n"
        "Your message will be sent directly to 2WAYARB support. "
        "You will receive a reply here."
    )

    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            reply_markup=keyboard,
        )
    else:
        await update.message.reply_text(
            message,
            reply_markup=keyboard,
        )


async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await support_prompt(update, context)


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    if query.data == "home":
        context.user_data.pop("support_mode", None)

        await query.edit_message_text(
            "Welcome to 2WAYARB — Relative Value Signals.\n\n"
            "No courses. No hype. Just the trades.\n\n"
            "Choose an option below:",
            reply_markup=main_menu(),
        )

    elif query.data == "support":
        await support_prompt(update, context)

    elif query.data == "what":
        context.user_data.pop("support_mode", None)

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⭐ Subscribe", url=PAID_LINK)],
            [InlineKeyboardButton("⬅️ Back", callback_data="home")],
        ])

        await query.edit_message_text(
            "📊 WHAT YOU GET\n\n"
            "• Real-time spread-arbitrage signals\n"
            "• Major indices as the primary focus\n"
            "• Selected FX opportunities\n"
            "• Entry and trade direction information\n"
            "• Signals delivered directly through Telegram\n\n"
            "No courses. No hype. Just signals.",
            reply_markup=keyboard,
        )

    elif query.data == "plans":
        context.user_data.pop("support_mode", None)

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⭐ Subscribe Now", url=PAID_LINK)],
            [InlineKeyboardButton("⬅️ Back", callback_data="home")],
        ])

        await query.edit_message_text(
            "💳 SUBSCRIPTION\n\n"
            "2WAYARB Monthly\n\n"
            "$40/month\n\n"
            "Payment and recurring access are handled "
            "through Telegram.",
            reply_markup=keyboard,
        )

    elif query.data == "about":
        context.user_data.pop("support_mode", None)

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back", callback_data="home")]
        ])

        await query.edit_message_text(
            "ℹ️ ABOUT 2WAYARB\n\n"
            "2WAYARB focuses on relative-value and "
            "spread-arbitrage opportunities, primarily "
            "across major indices and occasionally FX pairs.\n\n"
            "No training. No hype. Just signals.",
            reply_markup=keyboard,
        )

    elif query.data == "faq":
        context.user_data.pop("support_mode", None)

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⭐ Subscribe", url=PAID_LINK)],
            [InlineKeyboardButton("⬅️ Back", callback_data="home")],
        ])

        await query.edit_message_text(
            "❓ FAQ\n\n"
            "Q: How much is access?\n"
            "A: $40/month.\n\n"
            "Q: How do I subscribe?\n"
            "A: Tap Subscribe and complete the Telegram payment.\n\n"
            "Q: How do I receive signals?\n"
            "A: Signals are delivered inside the private "
            "2WAYARB channel.\n\n"
            "Q: Are profits guaranteed?\n"
            "A: No. Trading involves risk and profits are "
            "not guaranteed.",
            reply_markup=keyboard,
        )


async def message_router(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = update.message

    if not message:
        return

    user = update.effective_user
    user_id = user.id

    # ADMIN REPLY SYSTEM
    if user_id == ADMIN_CHAT_ID:
        if message.reply_to_message:
            replied_text = (
                message.reply_to_message.text
                or message.reply_to_message.caption
                or ""
            )

            match = re.search(r"User ID:\s*(\d+)", replied_text)

            if match:
                customer_id = int(match.group(1))

                try:
                    await context.bot.copy_message(
                        chat_id=customer_id,
                        from_chat_id=ADMIN_CHAT_ID,
                        message_id=message.message_id,
                    )

                    await message.reply_text(
                        "✅ Reply sent to the customer."
                    )

                except Exception:
                    logging.exception("Could not send admin reply")

                    await message.reply_text(
                        "❌ I couldn't deliver that reply to the customer."
                    )

        return

    # CUSTOMER SUPPORT SYSTEM
    if not context.user_data.get("support_mode"):
        return

    username = (
        f"@{user.username}"
        if user.username
        else "No username"
    )

    name = user.full_name or "Unknown"

    notification = (
        "🆘 NEW SUPPORT REQUEST\n\n"
        f"👤 Name: {name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 User ID: {user_id}\n\n"
        "💬 Customer message is below.\n\n"
        "↩️ Reply directly to THIS notification to respond."
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=notification,
        )

        await message.forward(
            chat_id=ADMIN_CHAT_ID,
        )

        await message.reply_text(
            "✅ Your message has been received.\n\n"
            "Support will reply to you here as soon as possible.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    "⬅️ Back to Menu",
                    callback_data="home"
                )]
            ]),
        )

    except Exception:
        logging.exception("Support request failed")

        await message.reply_text(
            "⚠️ Sorry, your support message could not be sent right now. "
            "Please try again."
        )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("subscribe", subscribe))
app.add_handler(CommandHandler("plans", plans))
app.add_handler(CommandHandler("about", about))
app.add_handler(CommandHandler("faq", faq))
app.add_handler(CommandHandler("support", support_command))

app.add_handler(CallbackQueryHandler(button_handler))

app.add_handler(
    MessageHandler(
        filters.ChatType.PRIVATE & ~filters.COMMAND,
        message_router,
    )
)

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path="telegram",
    webhook_url=WEBHOOK_URL,
    drop_pending_updates=True,
    )
