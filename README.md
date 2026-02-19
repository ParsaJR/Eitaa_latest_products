## Eitaa Product crawler


## Installation

### Docker-compose:
Fork the project:
```sh
git clone https://github.com/ParsaJR/Eitaa_latest_products
```

After that, use the `docker-compose.yaml` to setup the services.
__But before that, setup the proper environment variables__:
```
services:
  app:
    build: .
    environment:
      - LIARA_API_KEY=CHANGEME <-
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - redis
  redis:
    image: redis:alpine
    container_name: redis-alpine
    restart: unless-stopped
```

And after that:
```sh
docker compose up
```
Will does the job.

### Local environment
1. Fork the project
```sh
git clone https://github.com/ParsaJR/Eitaa_latest_products
```

2. Set a required environment variables in your environment. you can use the
local `.env` file, which should be located at the root project directory:

* `LIARA_API_KEY`: Used for ai assistant(gpt-4o-mini), thorugh the channels validation process
* `REDIS_HOST` & `REDIS_PORT`: Used as a job queue

3. Install the requirements and run the project, using the python toolchain:
```
pip install -r requirements.txt

python3 main.py
```

## Architecture 

The application uses modern Python features with a goal of enhancing the
developer experience. Dataclasses are living in the `eitaa_types.py`.

Most of the core functionality lives in the `eitaa.py` and `EitaaToolKit` class. It will
abstract away most of the scraping jargon and etc.

The Eitaa's preview web page is the only convenient place for reading the latest
channels posts. It is implemented in the `get_latest_messages_by_id` method.

Configuration managements(Envs) are managed in `config.py`, and it can be liberally
accessed by the entire application.

Also Ai functionality lives in `ai.py`

### Eitaa's global search
Through my own research, the Eitaa's global search feature doesn't have any
official/unoffical way to intract with an api. The `eitaayar toolkit` has a pretty
limited functionality that is only useful for certain kinds of task
(E.g. Sending messages automatically in your channels).

Scraping is an option. But "Eitaa Web" is mostly a javascript web application,
so it will not play well with classic scraping libraries, Because they are
mostly useful only when the target Endpoint includes Server-side generated
content. 

So, The only option that came to my mind was a tool called `selenium`. Which is
practical, but it ain't a fit to the project goals(Distrubuted Eitaa's search
engine) and time-constrains. I gave it a try and gave up after some point:
```

    def selenium_login_session(self):
        """Logs-in to the Eitaa's web app using the selenium's Firefox driver, for the goal
        of using the Global search feature."""

        raise NotImplementedError(
            """This method is currently incomplete. Eitaa's Global Search is
            barely accessable, even for it's own official clients."""
        )

        for phone_number in self.phone_numbers:
            print("Selenium is going to bootstrap. Please wait...")

            driver = webdriver.Firefox()
            driver.get("https://web.eitaa.com")
            wait = WebDriverWait(driver, 20)

```

As a result, i just gave up, and used a hardcoded usernames discovery phase.

It should be noted, The Eitaa's global search feature is barely useful even for
it's own official Web/Android clients. It's not just rare-limited. It seems
[broken by design](https://www.aparat.com/v/onf72hy?t=74). 

### Ai prompt

```

    You are an expert classifier helping me to validate telegram channels.

    Your task is :
    Determine whether the given channel is a shopping business channel or not.

    A shop channel typically:
    - Promotes products
    - Shows prices
    - Has purchase instructions
    - Contains product images

    Keep in mind that, the messages are in persian language. And i will send you
    three latest messages of that channel for you, to help you make sense of it.

    Respond ONLY with valid JSON in the following format:
    {
    "is_shop_channel": true OR false,
    }
	
```
This form of prompt enables us to act upon the response, programmically, and
without manual human interaction.
