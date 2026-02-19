import json

from attr import asdict

import eitaa
import redis_client


def main():

    # hard-coded channels.
    channel_ids: list[str] = ["amookafshdozak", "vibepinterest", "sh2386"]

    et = eitaa.EitaaToolKit(channel_ids=channel_ids)

    channels = et.fetch_and_iterate()

    validated_channels = et.validate(channels)

    print(f"{len(validated_channels)} Shopping channels has been confirmed: \n \n")

    list_name = "amadast_queue"
    for ch in channels:
        js = json.dumps(asdict(ch))
        _ = redis_client.redis_connection.rpush(list_name, js)

    print("🚀 The job queue has been flushed(completed) Bye!")
    exit(0)


if __name__ == "__main__":
    main()
