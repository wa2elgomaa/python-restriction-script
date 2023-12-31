from argparse import ArgumentParser
from sys import argv, executable
from datetime import datetime, timedelta
from subprocess import check_call
from dotenv import load_dotenv
from handler import Handler

load_dotenv()

offset = 0
limit = 100


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
    parser.add_argument(
        '-start-from', nargs='*', help='How many days backward i.e. 14.')
    parser.add_argument(
        '-end-to', nargs='*', help='How many days forward, should provide startfrom')
    parser.add_argument(
        '-upload-start-date', nargs='*', help='Uploaded start date to run the script manually')
    parser.add_argument(
        '-upload-end-date', nargs='*', help='Uploaded end date to run the script manually')

    args = parser.parse_args(args=argv[2:])

    env = args.env[0] if args.env is not None and len(args.env) > 0 else 'sandbox'
    debug = True if args.debug is not None else False
    start_from = args.start_from[0] if args.start_from is not None else 1
    end_to = args.end_to[0] if args.end_to is not None else 1
    upload_start_date = args.upload_start_date[0] if args.upload_start_date is not None else None
    upload_end_date = args.upload_end_date[0] if args.upload_end_date is not None else None
    handler = Handler(env, debug)

    # calculate the start and end date based on inputs
    calculated_date = (datetime.now() - timedelta(days=int(start_from))).replace(hour=0, minute=0, second=0)
    start_date = upload_start_date if upload_start_date is not None else int(calculated_date.timestamp() * 1000)
    # end_date = int(datetime.now().timestamp() * 1000)
    end_date = upload_end_date if upload_end_date is not None else int(
        (calculated_date + timedelta(days=int(end_to))).replace(hour=0, minute=0, second=0).timestamp() * 1000)

    empty = False
    # update photos list
    while empty is False:
        empty = handler.search(start_date, end_date).update()


if __name__ == '__main__':
    start_task()
