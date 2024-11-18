# python Library
import sys
import logging
import logging.config
import inspect
import os
from datetime import datetime

# Custom
from Generic.Messenger import Messenger

@DeprecationWarning
# Create own contextual information
class ContextFilter(logging.Filter):
    def filter(self, record):
        pass
        record.modname = "asdsa"
        # setattr(record, "modname", "asdsadasd")
        return True

class logger:

    def __init__(self, config_file=None):
        if(not config_file):
            config_file = self.__CONFIG_FILE_NAME()
        else:
            config_file = os.path.join(os.path.dirname(__file__), "logger.ini")
        print(config_file)
        self.config_logger_from_file(config_file)
        return None

    @DeprecationWarning
    def __initiate_logger(self, messenger_obj):
        """Initiate Logger will creates context filter and other initiation for logger

        Arguments:
            messenger_obj {Messenger}
                -- messenger_obj is an Inter-Process-Communication object which holds basic details for
                    interprocess communication

        Returns:
            Logger -- python logger object
        """

        # create logger
        logger = logging.getLogger()
        module = messenger_obj.module
        messenger_obj.success = True
        # Create contextual filter to add module to the handler
        filter_set = ContextFilter()
        logger.addFilter(filter_set)
        return logger

    def debug(self, messenger_obj=None, can_log=True):
        """debug - Writes a debug message into log file

        Keyword Arguments:
            messenger_obj {Messenger}
                -- Inter-Process-Communication Object which holds basic communication data
                    (default: {None})
            can_log {bool}
                -- Manually set whether to log the message (default: {True})

        Returns:
            [Messenger]
                -- Inter-Process-Communication Object which holds basic communication data
        """

        if(can_log):
            try:
                messenger_obj, logger = self.get_message(messenger_obj)
                logger.debug(str(messenger_obj.message))
            except Exception as e:
                print("Exception : " + str(e))
                # print(messenger_obj.message)
                messenger_obj.success = False
                

            finally:
                logging.shutdown()
        else:
            print('Manual log prevention - Activated')
        return messenger_obj

    def info(self, messenger_obj=None, can_log=True):
        """info - Writes a info message into log file

        Keyword Arguments:
            messenger_obj {Messenger}
                -- Inter-Process-Communication Object which holds basic communication data
                    (default: {None})
            can_log {bool}
                -- Manually set whether to log the message (default: {True})

        Returns:
            [Messenger]
                -- Inter-Process-Communication Object which holds basic communication data
        """

        if(can_log):
            try:
                messenger_obj, logger = self.get_message(messenger_obj)
                logger.info(str(messenger_obj.message))
            except Exception as e:
                messenger_obj.success = False
                

            finally:
                logging.shutdown()
        else:
            print('Manual log prevention - Activated')
        return messenger_obj

    def error(self, messenger_obj=None, can_log=True):
        """error - Writes a error message into log file

        Keyword Arguments:
            messenger_obj {Messenger}
                -- Inter-Process-Communication Object which holds basic communication data
                    (default: {None})
            can_log {bool}
                -- Manually set whether to log the message (default: {True})

        Returns:
            [Messenger]
                -- Inter-Process-Communication Object which holds basic communication data
        """
        if(can_log):
            try:
                messenger_obj, logger = self.get_message(messenger_obj)
                logger.error(str(messenger_obj.message))
            except Exception as e:
                messenger_obj.success = False
            finally:
                logging.shutdown()
        else:
            print('Manual log prevention - Activated')
        return messenger_obj

    def warning(self, messenger_obj=None, can_log=True):
        """warning - Writes a warning message into log file

        Keyword Arguments:
            messenger_obj {Messenger}
                -- Inter-Process-Communication Object which holds basic communication data
                    (default: {None})
            can_log {bool}
                -- Manually set whether to log the message (default: {True})

        Returns:
            [Messenger]
                -- Inter-Process-Communication Object which holds basic communication data
        """
        if(can_log):
            try:
                messenger_obj, logger = self.get_message(messenger_obj)
                logger.warning(str(messenger_obj.message))
            except Exception as e:
                messenger_obj.success = False
                

            finally:
                logging.shutdown()
        else:
            print('Manual log prevention - Activated')
        return messenger_obj

    def critical(self, messenger_obj=None, can_log=True):
        """critical - Writes a critical message into log file

        Keyword Arguments:
            messenger_obj {Messenger}
                -- Inter-Process-Communication Object which holds basic communication data
                    (default: {None})
            can_log {bool}
                -- Manually set whether to log the message (default: {True})

        Returns:
            [Messenger]
                -- Inter-Process-Communication Object which holds basic communication data
        """
        if(can_log):
            try:
                messenger_obj, logger = self.get_message(messenger_obj)
                logger.critical(str(messenger_obj.message))
            except Exception as e:
                messenger_obj.success = False
                # 
                
            finally:
                logging.shutdown()
        else:
            print('Manual log prevention - Activated')
        return messenger_obj

    def write_default_log(self, messenger_obj=None, can_log=True):
        """write_default_log - Writes a message into log file, based on given
                                log level

        Keyword Arguments:
            messenger_obj {Messenger}
                -- Inter-Process-Communication Object which holds basic communication data
                    (default: {None})
            can_log {bool}
                -- Manually set whether to log the message (default: {True})

        Returns:
            [Messenger]
                -- Inter-Process-Communication Object which holds basic communication data
        """
        if(can_log):
            try:
                logger = self.__initiate_logger(messenger_obj)
                error_level = messenger_obj.level.lower()
                message = messenger_obj.message
                filter_set = ContextFilter()
                logger.addFilter(filter_set)

                if error_level == 'debug':
                    logger.debug(str(message))
                elif error_level == 'info':
                    logger.info(str(message))
                elif error_level == 'warn':
                    logger.warning(str(message))
                elif error_level == 'error':
                    logger.error(str(message))
                elif error_level == 'critical':
                    logger.critical(str(message))
                else:
                    logger.critical('Unable to find the error level described')

            except Exception as e:
                messenger_obj.success = False
                
            finally:
                logging.shutdown()
        else:
            print('Manual log prevention - Activated')
        return messenger_obj

    def __write_log_exception(self, e):
        """__write_log_exception - Writes exception log for Logger occurs

        Returns:
            [Messenger]
                -- Inter-Process-Communication Object which holds basic communication data
        """
        print("HITS")
        
        called_function_name = self.get_called_function_name()
        messenger_obj = Messenger()
        messenger_obj.module = 'Logger'
        messenger_obj.message = 'Unable to load Logger/ Logger not available in '
        messenger_obj.message = messenger_obj.message + called_function_name
        self.critical(messenger_obj)

        return messenger_obj

    def get_called_funciton_name_with_module(self):
        innerframe = inspect.currentframe()
        outerframes = inspect.getouterframes(innerframe)

        for index, frame in enumerate(outerframes):
            # print(index, frame)
            if(frame.function == "get_called_funciton_name_with_module"):
                index += 6
                break
        # print(index, outerframes[index])
        called_function_name = (outerframes[index].function)
        if(called_function_name != "<module>"):
            called_function_name += "()"
        module_name = self.__get_bot_name__(outerframes[index].filename)
        called_function_name = str(module_name + '.' + called_function_name)

        return called_function_name

    def get_called_function_name(self):
        innerframe = inspect.currentframe()
        outerframes = inspect.getouterframes(innerframe)

        for index, frame in enumerate(outerframes):
            if(frame.function == "get_called_function_name"):
                index += 2
                break

        called_function_name = (outerframes[index].function)
        if(called_function_name != "<module>"):
            called_function_name += "()"

        return called_function_name

    def __get_parent_directory(self, file_name):
        expanded_dir = os.path.expanduser(file_name)
        realpath_dir = os.path.realpath(expanded_dir)
        directory = os.path.dirname(realpath_dir)
        return directory

    def __CONFIG_FILE_NAME(self):
        log_path = self.__get_parent_directory(__file__)
        if(os.path.exists(log_path)):
            return os.path.join(log_path, 'logger.ini')
        else:
            return os.path.join(os.getcwd(), 'logger.ini')

    def __get_bot_name__(self, file_name):
        return os.path.splitext(self.__get_file_name__(file_name))[0]

    def __get_file_name__(self, file_name):
        return os.path.basename(file_name)

    def get_logfile(self):
        return datetime.strftime(datetime.now() ,"%Y-%m-%d")

    def config_logger_from_file(self, config_file):
        self.get_logfile()
        debug_folder = os.path.join(os.environ["LOGS_PATH"], "debug")
        error_folder = os.path.join(os.environ["LOGS_PATH"], "error")
        if(not os.path.exists(debug_folder)):
            os.makedirs(debug_folder)
        if(not os.path.exists(error_folder)):
            os.makedirs(error_folder)
        logging.config.fileConfig(config_file, defaults={
            "debugfilename": os.path.join(debug_folder, self.get_logfile() + "-debug.log"),
            "errorfilename": os.path.join(error_folder, self.get_logfile() + "-error.log")
        })
        return None

    def get_message(self, messenger_obj):
        # extra = {'modname': messenger_obj.module + " | " + messenger_obj.fun_name}
        module = messenger_obj.module
        fun_name = self.get_called_funciton_name_with_module()
        logger = logging.getLogger(module + " | " + fun_name)
        logger = logging.LoggerAdapter(logger, extra={})
        # logger.setLevel(logging.ERROR)
        # if messenger_obj.data:
        #     messenger_obj.data['method_name'] = self.get_called_function_name()
        #     messenger_obj.message = "{messenger_obj.module} | " + messenger_obj.message
        #     messenger_obj.message = messenger_obj.message.format(messenger_obj=messenger_obj)
        return messenger_obj, logger
