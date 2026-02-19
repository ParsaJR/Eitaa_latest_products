from openai import OpenAI
import json

from typing import TypedDict
import config
from eitaa_types import Channel

if config.liara_api_key is None:
    raise ValueError("liara_api_key must be set")

client = OpenAI(
    api_key=config.liara_api_key,
    base_url="https://ai.liara.ir/api/6995a24052fea26d57ac7a3d/v1",
)


class ChannelClassification(TypedDict):
    is_shop_channel: bool


def classify_channel(channel: Channel) -> bool:
    """
    Asks an external system for helping through the channel validation process.
    Returns an dict that has a single key, named: 'is_shop_channel'.
    """

    system_prompt = """
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
    """

    three_last_messages = {
        "0": channel.messages[-1],
        "1": channel.messages[-2],
        "2": channel.messages[-3],
    }

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(three_last_messages)},
        ],
    )

    if not response.choices[0].message.content:
        raise Exception("No response from liara's api.")

    result: ChannelClassification = json.loads(response.choices[0].message.content)
    print(result)

    return result["is_shop_channel"]
