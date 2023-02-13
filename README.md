# Django Telegram bo


> This project is fork of [dj-ms-core](https://github.com/dj-ms/dj-ms-core).
> The main documentation is kept there.
> 
> Here is only the documentation related directly to the Telegram bot.


> When setting up project, just add `TELEGRAM_TOKEN` environment variable with your Telegram bot token.


## Purpose

This project is inspired by [ohld/django-telegram-bot](https://github.com/ohld/django-telegram-bot).

The main difference is that this project aims to be more flexible and to provide more features.
For example, Django's translation system is used to provide multilingual support.


## Getting started

1. Fork this project.
2. Set it up and run according to the [dj-ms-core documentation](https://github.com/dj-ms/dj-ms-core/blob/master/README.md).
3. Look at example bots in `app/bot/workers` directory. Example files are named `example_*`.
4. Create you own bot in `app/bot/workers` directory. You can use `example_*` files as a template.
5. In `app.bot.dispatcher.py` change import of Worker class to your bot class.
    <br>
    Comment out the line:
    <br>
    ```python
    from app.bot.workers.example_main import Worker
    ```
    <br>
    and add your bot class:
    <br>
    ```python
    from app.bot.workers.your_bot import Worker
    ```
6. Run the project and test your bot.