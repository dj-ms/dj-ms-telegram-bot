# Django Telegram bot


> This project is fork of [dj-ms-core](https://github.com/dj-ms/dj-ms-core).
> The main documentation is kept there.
> 
> Here is only the documentation related directly to the Telegram bot.

## Screenshots
|                        |                        |                        |
|:----------------------:|:----------------------:|-----------------------:|
| ![](/docs/media/1.png) | ![](/docs/media/2.png) | ![](/docs/media/3.png) |

## About

This project is inspired by [ohld/django-telegram-bot](https://github.com/ohld/django-telegram-bot).
Like the original project, it is:
- based on [python-telegram-bot](https://python-telegram-bot.org/).
- uses Django as a web framework.
- uses Celery as a task queue.
- uses PostgreSQL as a database.
- uses Redis as a cache.
- uses Docker and Docker Compose for development and deployment.

Additionally, what was added:
- multilingual support (using Django's translation system).
- microservice architecture support (using [dj-ms-core](https://github.com/dj-ms/dj-ms-core)).
- Implementation of some features, such as nested menus.
- RabbitMQ as a message broker (from `dj-ms-core`).
- Kubernetes support (from `dj-ms-core`).

The main difference is that this project aims to be more flexible and to provide more features.
For example, Django's translation system is used to provide multilingual support.


## Getting started

### Independent bot

> Note: This project is not yet ready for production, like the original project.
> Please, use it only for testing and development. It will be ready for production with release of version 1.0.0.

1. Fork this project.

2. Set it up and run according to the [dj-ms-core documentation](https://github.com/dj-ms/dj-ms-core/blob/master/README.md).
    > When setting up project, just add `TELEGRAM_TOKEN` environment variable with your Telegram bot token.

3. Look at example bots in `app/bot/workers` directory. Example files are named `example_*`.

4. Create you own bot in `app/bot/workers` directory. You can use `example_*` files as a template.

5. In `app.bot.dispatcher.py` change import of Worker class to your bot class.

    Comment out the line:

    ```
    from app.bot.workers.example_main import Worker
    ```

    and add your bot class:

    ```
    from app.bot.workers.your_bot import Worker
    ```

6. Run the project and test your bot.


### Microservice

1. Fork this project.

2. Set it up and run according to the [dj-ms-core documentation](https://github.com/dj-ms/dj-ms-core/blob/master/README.md).
    > When setting up project, add next variables:
    > - `TELEGRAM_TOKEN` environment variable with your Telegram bot token
    > - DJ_MS_APP_LABEL=telegram-bot 
    > - AUTH_DB_URL=postgres://postgres:postgres@`<MAIN_SERVICE_HOST>``<MAIN_DB_PORT>`/postgres 
    > - BROKER_URL=amqp://rabbitmq:rabbitmq@`<MAIN_SERVICE_HOST>``<MAIN_RABBITMQ_PORT>`
