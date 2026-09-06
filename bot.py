import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]

PAID_LINK = "https://t.me/+CzC7KBjLbDhkNDlk"

# Change this later to your actual support username.
SUPPORT_USERNAME = "2WAYARB_SUPPORT"


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
    text = (
        "Welcome to 2WAYARB — Relative Value Signals.\n\n"
        "Real-time spread-arbitrage signals focused primarily "
        "on major indices, with selected FX opportunities.\n\n"
        "No courses. No hype. Just the trades.\n\n"
        "Choose an option below:"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ Subscribe Now", url=PAID_LINK)],
        [InlineKeyboardButton("⬅️ Back", callback_data="home")]
    ])

    await update.message.reply_text(
        "⭐ 2WAYARB Monthly Access\n\n"
        "Subscription: $40/month\n\n"
        "Tap below to subscribe and receive access "
        "to the private 2WAYARB channel.",
        reply_markup=keyboard
    )


async def plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await subscribe(update, context)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ ABOUT 2WAYARB\n\n"
        "2WAYARB focuses on relative-value and "
        "spread-arbitrage opportunities, primarily "
        "across major indices and occasionally FX pairs.\n\n"
        "No training. No hype. Just signals."
    )


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 SUPPORT\n\n"
        "For subscription or access issues, contact:\n\n"
        f"https://t.me/{SUPPORT_USERNAME}"
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    if query.data == "home":

        await query.edit_message_text(
            "Welcome to 2WAYARB — Relative Value Signals.\n\n"
            "No courses. No hype. Just the trades.\n\n"
            "Choose an option below:",
            reply_markup=main_menu()
        )

    elif query.data == "what":

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⭐ Subscribe", url=PAID_LINK)],
            [InlineKeyboardButton("⬅️ Back", callback_data="home")]
        ])

        await query.edit_message_text(
            "📊 WHAT YOU GET\n\n"
            "• Real-time spread-arbitrage signals\n"
