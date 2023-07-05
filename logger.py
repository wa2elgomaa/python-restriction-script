from os import makedirs, path
from traceback import format_exception
from datetime import datetime


class Logger:
    logs_folder = 'restriction-logs'
    logs_file_prefix = 'logs-'

    def __init__(self):
        self.logs_folder = 'restriction-logs'
        self.logs_file_prefix = 'logs-'

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
        print(f'---LOG--- {message}')

        # create logs folder if not exists
        self.create_folder(self.logs_folder)
        # log the error in a separate file
        with open(f'{self.logs_folder}/{self.logs_file_prefix}{datetime.today().strftime("%Y-%m-%d")}.txt', 'a+',
                  encoding='utf-8') as f:
            # Move read cursor to the start of file.
            f.seek(0)
            # If file is not empty then append '\n'
            txt = f.read(100)
            if len(txt) > 0:
                f.write('\n')
            f.write(message)
            if e:
                f.write('\n')
                f.write(f'Error : {self.get_traceback(e)}')
            f.close()
