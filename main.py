import os
import logging
import time
import signal

from dependency_injector.wiring import inject, Provide
from dependency_injector.providers import Configuration, Singleton
from prometheus_client import start_http_server

from bootstrap import Container
# from models.db import Database
from infra.tg_bot import TGBot
# from controllers.loop import loop_step
from metrics import metrics


LOOP_DELAY = 5 * 60
METRICS_PORT = 2112

def start_metrics():
    """
    Start metrics server
    """
    logging.info("Starting metrics server in port: {}".format(METRICS_PORT))
    start_http_server(METRICS_PORT)

def setup_di(config_path: str):
    """
    Setup dependency injection
    """
    container = Container()
    container.conf.from_yaml(config_path)
    container.bot.override(Singleton(TGBot, tg_bot_token=container.conf.tg_bot_token,
                                            stripe_token=container.conf.stripe_token))
    container.wire(modules=[__name__], packages=['app.models', 'app.controllers', 'infra', 'core'])

def setup_signal_handler(bot):

    def _signal_handler(signum, frame):
        logging.info("Received signal %d, exiting...", signum)
        bot.stop()
        bot.working = False
        print('bye bye!')
        exit(0)

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)


@inject    
def main(bot: TGBot = Provide[Container.bot],
        #  db: Database = Provide[Container.db],
         conf: Configuration = Provide[Container.conf]):
    """
    Main entry point for the bot.
    """
    level = logging.INFO if conf['logging_level'].lower() == 'info' else logging.DEBUG
    logging.basicConfig(level=level,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    start_metrics()
    bot.working = True
    bot.register()
    setup_signal_handler(bot)
    bot.start()
    while bot.working:
        try:
            metrics.MAIN_LOOP_TICKS.inc()
            # Do something awesomic!
            logging.info('>>> Main loop step. Perform smalls tasks here!')
        except Exception as ex:
            logging.warn("Unexpected exception: {}".format(ex))
            metrics.MAIN_LOOP_EXCEPTION.inc()
        time.sleep(LOOP_DELAY)
    bot.stop()

if __name__ == '__main__':
    config_path = os.environ.get('BOT_CONFIG', 'config.yaml')
    setup_di(config_path)
    main()
