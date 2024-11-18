from . import datetime, os, stat
from time import sleep
import sys
from time import sleep
start_time = datetime.now()
from .package import logger, Messenger
# from Generic.Log import Logger
# from Generic.Messenger import Messenger
# # from ..Logger import Logger
# from .. import Constants as const
# The base class covers most utilities functions
class Utilities:
    
    LOGS = {
        "DEBUG": 1,
        "INFO": 2,
        "WARNING": 3,
        "CRITICAL": 4,
        "ERROR": 5
    }
    LOG_TYPE = ""

    def __init__(self, **kwargs):
        self.messenger = Messenger()
        if "botname" in kwargs:
            module = kwargs["botname"]
        else:
            module = "UNKNOWN"
        if "log_type" in kwargs:
            self.LOG_TYPE = kwargs["log_type"]
        else:
            self.LOG_TYPE = "DEBUG"
        self.messenger.module = module

        # logger = logger
        # if(not log_file):
        #     t= datetime.now()
        #     log_dir = os.path.join(const.LOGS_PATH, t.strftime("%Y/%m/"))
        #     log_file = log_dir + t.strftime("%d")+ ".log"
        # else:
        #     log_dir = os.path.dirname(os.path.abspath(log_file))

        # self.check_and_create_dir(log_dir)
        # logger = Logger(log_file).get_logger(name)
        # os.chmod(log_file, 0o770)
        # uid = os.stat(log_file).st_uid
        # os.chown(log_file,uid,4)
    
    def set_log_type(self, log_type):
        self.LOG_TYPE = log_type

    # set_logger
    # * If a logger object exist use that as logger for this class
    # @param logger     - Logger object
    # @return None
    def set_logger(self, logger):
        self.logger = logger

    # print_info_log
    # * Prints output in console and logs it in log file
    # @param messenger    - Message to be written in console and log file
    # @return None
    def print_info_log(self, *message):
        self.log("INFO", *message)

    # print_warning_log
    # * Prints output in console and logs it in log file
    # @param messenger    - Message to be written in console and log file
    # @return None
    def print_warning_log(self, *message):
        self.log("WARNING", *message)

    # print_critical_log
    # * Prints output in console and logs it in log file
    # @param messenger    - Message to be written in console and log file
    # @return None
    def print_critical_log(self, *message):
        self.log("CRITICAL", *message)

    # print_error_log
    # * Prints output in console and logs it in log file
    # @param messenger    - Message to be written in console and log file
    # @return None
    def print_error_log(self, *message):
        self.log("ERROR", *message)

    # print_debug_log
    # * Prints output in console and logs it in log file
    # @param messenger    - Message to be written in console and log file
    # @return None
    def print_debug_log(self, *message):
        self.log("DEBUG", *message)

    # log
    # * Logs given message in Log file
    # @param message    - Message to be written in log file
    # @return None
    def log(self, log_type="", *message):
        if not log_type:
            print(*message)
            return
        for msg in message:
            if isinstance(msg, str):
                self.log_per_type(msg, log_type)
            elif isinstance(msg, list):
                for lmsg in msg:
                    self.log_per_type(lmsg, log_type)


    def log_per_type(self, message, log_type=""):
        try:
            if self.LOGS[log_type] >= self.LOGS[self.LOG_TYPE]:
                print(log_type.upper() + ": " + message)
            self.messenger.message = message
            if log_type.lower() == "info":
                logger.info(self.messenger)
            elif log_type.lower() == "debug":
                logger.debug(self.messenger)
            elif log_type.lower() == "error":
                logger.error(self.messenger)
            elif log_type.lower() == "warning":
                logger.warning(self.messenger)
            elif log_type.lower() == "critical":
                logger.critical(self.messenger)
            else:
                print(message)
        except OSError:
            pass
        except Exception as e:
            print(f"Utilities.log_per_type Error: {e}")

    # check_and_log_errors
    # * Checks Error array and logs them
    # @param e          - Error collection
    # @param header     - Header to be written in log file
    # @return None
    def check_and_log_errors(self, e=None, header="Error: "):
        if(e):
            if(len(e)>0):
                self.print_error_log(header + "\n".join(str(x) for x in e))
        else:
            self.print_error_log(header)

    # file_exists
    # * Checks if a file exists in the given path
    # @param file_path  - Path of the file to check
    # @return bool
    def file_exists(self, file_path):
        return os.path.exists(file_path)

    # check_and_create_dir
    # * Checks if the folder exists, if not create a folder in the location
    # @param full_path  - Full path of the folder to be created
    # @return None
    def check_and_create_dir(self, full_path):
        if(not self.file_exists(full_path)):
            os.makedirs(full_path)

    # check_args
    # * check if correct number of arguments are given
    # @param min_length     - Minimum number of expected arguments
    # @param error_response - Error message to be displayed in case
    # @return None
    def check_args(self, min_length, error_response):
        if(len(sys.argv) <= min_length):
            self.print_info_log(error_response)
            sys.exit(0)

    # decode
    # * Decodes a byte to ("UTF-8") String
    # @param message    - Message to be decoded
    # @return String
    def decode(self, message):
        return message.decode("utf-8").strip()
    
    def time_elapsed():
        return datetime.now() - start_time

    def sleep(self, sleep_time=1, message=None):
        if message:
            self.print_debug_log(f"Sleeping for {sleep_time}, Reason: {message}")
        sleep(sleep_time)
