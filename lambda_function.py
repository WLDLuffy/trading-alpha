import json
from app import run_cron, connect_binance


def lambda_handler(event, context):
    # TODO Implement
    print("event", event)
    print("context", context)

    binance_client = connect_binance()
    run_cron(binance_client)

    return {
        'statusCode': 200,
        'body': json.dumps("test")
    }
