from os import makedirs, path
from traceback import format_exception
from datetime import datetime, time


class Logger:
    def __init__(self, debug_mode=False):
        self.logs_folder = 'restriction-logs'
        self.logs_file_prefix = 'logs-'
        self.debug = debug_mode

    def create_folder(self, output_folder):
        # create output folder if not exists
        try:
            exists = path.exists(output_folder)
            if not exists and output_folder:
                makedirs(output_folder)
        except Exception as e:
            msg = f'--LOG-- ERR CREATING FOLDER {output_folder}'
            self.log_message(msg, e)

    def get_traceback(ex, ex_traceback=None):
        if ex is None:
            return 'Undefined Error'
        if ex_traceback is None:
            ex_traceback = ex.__traceback__
        return format_exception(ex.__class__, ex, ex_traceback)

    def log_message(self, message, e=None):
        log_msg = f'{datetime.now()} : ---LOG--- {message}'
        print(log_msg)
        if self.debug and e is not None:
            print(f'{datetime.now().strftime("%Y-%m-%d")} : Exception ', e)
        # create logs folder if not exists
        self.create_folder(self.logs_folder)
        # log the error in a separate file
        with open(f'{self.logs_folder}/{self.logs_file_prefix}{datetime.now().strftime("%Y-%m-%d")}.txt', 'a+',
                  encoding='utf-8') as f:
            # Move read cursor to the start of file.
            f.seek(0)
            # If file is not empty then append '\n'
            txt = f.read(100)
            if len(txt) > 0:
                f.write('\n')
            f.write(log_msg)
            if e:
                f.write('\n')
                f.write(f'Error : {self.get_traceback(e)}')
            f.close()
