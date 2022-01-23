import os
from typing import Any, Dict, Optional

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.context.ack import Ack
from slack_bolt.context.respond import Respond
from slack_bolt.error import BoltError

import light_sensor

#import logging
# logging.basicConfig(level=logging.DEBUG) # debug mode

app = App(token=os.environ.get('SLACK_BOT_TOKEN'))


@app.command('/boushitsu')
def respond_to_boushitsu(ack: Ack, respond: Respond, command: Optional[Dict[str, Any]]) -> None:
    '''respond to `/boushitsu`

        respond() calls `chat.postEphemeral`
        https://slack.dev/bolt-python/concepts#commands
        https://api.slack.com/interactivity/slash-commands
    '''

    ack()  # acknowledge

    # print(command)

    text = ''
    if light_sensor.is_open():
        text = 'boushitsu status: *open* :heavy_check_mark:'
    else:
        text = 'boushitsu status: *closed* :zzz:'

    msg = {
        'text': 'from boushitsu',
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': text
                },
                'accessory': {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Dismiss'
                    },
                    'action_id': 'dismiss'
                }
            }
        ]
    }

    respond(msg)  # send an ephemeral message


@app.block_action('dismiss')
def handle_dismiss_action(ack: Ack, respond: Respond) -> None:
    ack()
    respond(delete_original=True)


if __name__ == '__main__':
    try:
        handler = SocketModeHandler(app, os.environ.get('SLACK_APP_TOKEN'))
        handler.start()
    except KeyboardInterrupt:
        pass
    finally:
        light_sensor.cleanup()
