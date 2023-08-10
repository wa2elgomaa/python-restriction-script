from argparse import ArgumentParser
from sys import argv, executable
from datetime import datetime, timedelta
from subprocess import check_call
from dotenv import load_dotenv
from handler import Handler

load_dotenv()

offset = 0
limit = 100
days = 1


def install():
    check_call([executable, "-m", "pip", "install", '-r', './requirements.txt'])


def start_task():
    # user inputs
    parser = ArgumentParser(
        prog='XML Script', description='Updating XML files per folder updates')
    parser.add_argument(
        '-env', nargs='*', help='A folder contains NewsML XML files.')
    parser.add_argument(
        '-debug', nargs='*', help='Enable debug mode.')

    args = parser.parse_args(args=argv[2:])
    env = args.env[0] if args.env is not None and len(args.env) > 0 else 'sandbox'
    debug = args.debug[0] if args.debug is not None and len(args.debug) > 0 else False
    # photo center wrapper
    handler = Handler(env, debug)
    # start date 1 month back
    start_date = int((datetime.now() - timedelta(days=days)).replace(hour=0, minute=0).timestamp() * 1000)
    # end date now
    end_date = int(datetime.now().timestamp() * 1000)

    empty = False

    # update photos list
    while empty is False:
        empty = handler.search(start_date, end_date).update()


if __name__ == '__main__':
    start_task()
