# Telegram Bot Bootstrap

![Telegram Bot Bootstrap logo](doc/telegram-bot-bootstrap.jpg?raw=true)

## Introduction

Telegram bots are everywhere. Telegram Bot APIs let you create bots with a lot of features.
There are a lots of libraries for the most used languages: Python, PHP, JavaScripts, ...

In Python, `python-telegram-bot` is very used for it. This perfectly wraps Telegram's Bot APIs.

## Motivation

Despite `python-telegram-bot` is a great library for starting a new Telegram bot, to create a production grade ready telegram bot is necessary several dependencies, helpers, structure, ...

This bootstrap includes everything that you need to create an awesome Telegram bot quickly.

## Features

The major features of this bootstrap are:

- __Dependency injection__: You can easy inject dependencies for your bot.
- __Clean Architecture__: Approach to a clean architecture.
- __Internationalization (i18n) support__: `gettext` locale ready.
- __Persistence with database support__: Database support with SQLAlchemy and pydantic. 
- __Bot encapsulation__: Use of `class` instead of `methods` to interface with `python-telegram-bot`.
- __Payment ready__: If you can use Payments, a template handler for payments with Stripe is already enabled.
- __Execution lifecycle__: Use of `signals` to shutdown the bot properly.

## How to use

Clone this project, create a new Telegram Bot using Telegram Botfather bot, specify the tokens and implement your own commands.

1. Clone this repository
2. Follow this guide to create a new Telegram bot.
3. Prepare environment
4. Specify 

## Structure

- requirements.txt: Python packages requirements.
- main.py: Bot entry point.
- config.yaml: Configuration parameters.
- Dockerfile: Dockerfile for docker image generation.
  

## I18N

This project use `gettext`for i18n.
With `makemessages.sh` it create the translation files. 
Compile the messages with `compilemessages.sh`.

## Status

This project is under heavy development right now. Some components may suffer big changes in the near/middle future. 

## Contribute 

If you like to contribute or discuss about design, features, ... issues and PRs are welcome :)

## Roadmap

- Metrics reporting with Prometheus (WIP)
- Webhook mode
- FSM (initiated)
  
## License

Apache 2.0 License
