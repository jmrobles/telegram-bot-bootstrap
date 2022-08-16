import logging
import dataclasses

from telegram import KeyboardButton, LabeledPrice, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PreCheckoutQueryHandler


from utils import get_trans, get_random_quote

# i18n decorator
def i18n(fn):

    def inner(self, update, context):
        _ = get_trans(update.effective_user.language_code)
        fn(self, update, context, _)
    return inner


@dataclasses.dataclass
class TGBot():

    def __init__(self, tg_bot_token: str, stripe_token: str = None):

        self.tg_bot_token = tg_bot_token
        self.stripe_token = stripe_token

    def register(self):
        self.updater = Updater(self.tg_bot_token, use_context=True)
        dp = self.updater.dispatcher
        dp.logger.info("Bot started")
        # Commands
        dp.add_handler(CommandHandler('start', self.tg_start, run_async=True))
        dp.add_handler(CommandHandler('quote', self.tg_quote, run_async=True))
        dp.add_handler(MessageHandler(Filters.text, self.tg_message, run_async=True))
        # Hack: show menu button
        cmds = {'en': [
                        {'command': 'start', 'description': 'Start to using this bot'},
                        {'command': 'quote', 'description': 'Get an inspirational quote!'},
                    ],
                'es': [
                        {'command': 'start', 'description': 'Comienza a usar este bot'},
                        {'command': 'quote', 'description': '¡Obtén una cita inspiradora!'},
                    
                ]
        }
        dp.bot._post("setMyCommands", {'commands': cmds['en'], 'language_code': 'en'})
        dp.bot._post("setMyCommands", {'commands': cmds['es'], 'language_code': 'es'})
        dp.bot._post("setChatMenuButton", {'menu_button': {'type': 'commands'}})

        # -- Flow for payments
        # Un-comment to enable it
        # dp.add_handler(PreCheckoutQueryHandler(self.tg_precheckout_callback, run_async=True))
        # dp.add_handler(MessageHandler(Filters.successful_payment, self.tg_successful_payment_callback, run_async=True))

        
    def start(self):

        self.updater.start_polling()

    def stop(self):

        self.updater.stop()

    def send_message(self, chat_id: int, text: str):

        self.updater.bot.send_message(chat_id, text)

    # /start command
    @i18n
    def tg_start(self, update, context, _):
        context.bot.send_message(chat_id=update.effective_chat.id, text=_("start_cmd_answer"))

    # /quote command
    @i18n
    def tg_quote(self, update, context, _):
        context.bot.send_message(chat_id=update.effective_chat.id, text=get_random_quote())

    # Message handler
    @i18n
    def tg_message(self, update, context, _):
        """
        Message handler
        """
        logging.info('Generic message handler: {}'.format(update.message.text))    


    # /subscribe command
    # @i18n
    # def tg_subscribe(self, update, context, _):
    #     chat_id = update.message.chat_id
    #     title = _("cmd_subscribe_title")
    #     description = _("cmd_subscribe_description")
    #     payload = "subs_001"
    #     currency = "USD"
    #     price = 4
    #     # price * 100 so as to include 2 decimal points
    #     prices = [LabeledPrice(_("subscription_base"), price * 100)]
    #     context.bot.send_invoice(
    #         chat_id, title, description, payload, self.stripe_token, currency, prices)

    # @i18n
    # def tg_precheckout_callback(self, update, context, _):
    #     logging.info("precheckout_callback: {}".format(update.to_dict()))
    #     query = update.pre_checkout_query
    #     # check the payload, is this from your bot?
    #     if query.invoice_payload != 'subs_001':
    #         # answer False pre_checkout_query
    #         query.answer(ok=False, error_message=_("precheckout_error"))
    #     elif already_subscribed(update.effective_user.id, update.effective_user.language_code):
    #         query.answer(ok=False, error_message=_("precheckout_already_error"))
    #     else:
    #         query.answer(ok=True)

    # @i18n
    # def tg_successful_payment_callback(self, update, context, _):
    #     logging.info("Payment successful: {}".format(update.message.successful_payment))
    #     logging.info("chat id: {}".format(update.message.chat_id))
    #     responses = upgrade_subscription(update.message.chat_id, update.effective_user.language_code,
    #                                      update.message.successful_payment, _)
    #     for response in responses:
    #         context.bot.send_message(chat_id=update.effective_chat.id, text=response)
