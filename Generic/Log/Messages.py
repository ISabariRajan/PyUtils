INFO_PACKAGE_LOAD = "Package {ipc_object.data[package_name]} loaded"
INFO_BOT_LOAD = "Bot loaded"
INFO_BOT_COMPLETED = "Bot {ipc_object.data[bot_name]} completed"

ERROR_STRING = "\nError: {ipc_object.data[error]}"
ERROR_BOT_LOAD = "Error loading bot {ipc_object.data[bot_name]}"
ERROR_PACKAGE_LOAD = str("Error loading package {ipc_object.data[package_name]}" +
    ERROR_STRING)
ERROR_READ_ARGUMENT = str("Error reading argument" +
    ERROR_STRING)
ERROR_READ_CONFIG_FILE = str("Error reading configuration at {ipc_object.data[file_name]}" +
    ERROR_STRING)
ERROR_REPORT_GENERATION = str("Error when generating report {ipc_object.data[file_name]}")
ERROR_IN_METHOD = str("Error in {ipc_object.data[method_name]}" + ERROR_STRING)
ERROR_CONNECTING_DATABASE = str("Error while connecting database" +
    ERROR_STRING)
ERROR_DATA_FETCH = str("Error while fetching data" +
    ERROR_STRING)
ERROR_SENDING_MAIL = str("Error sending mail" + ERROR_STRING)
ERROR_FILE_READ = str("Error when reading file" + ERROR_STRING)
ERROR_FILE_WRITE = str("Error when writing file" + ERROR_STRING)
ERROR_FILE_ATTACH = str("Error attaching file" + ERROR_STRING)
ERROR_IN_FILE_PATH = str("Error in file path" + ERROR_STRING)

DEBUG_FILE_READ_COMPLETED = "{ipc_object.data[file_name]} read operation completed"
DEBUG_FILE_WRITE_COMPLETED = "{ipc_object.data[file_name]} write operation completed"
DEBUG_CONFIG_FILE_READ_COMPLETED = "Config file - " + DEBUG_FILE_READ_COMPLETED
DEBUG_CONFIG_FILE_WRITE_COMPLETED = "Config file - " + DEBUG_FILE_WRITE_COMPLETED
DEBUG_REPORT_FILE_WRITE_COMPLETED = "Report file - " + DEBUG_FILE_WRITE_COMPLETED
DEBUG_ARGUMENT_READ_COMPLETED = "Argument read completed"
DEBUG_METHOD_INITIATED = "{ipc_object.data[method_name]} initiated"
DEBUG_METHOD_COMPLETED = "{ipc_object.data[method_name]} completed"
DEBUG_FILE_ATTACHMENT_SUCCESS = "File attachment success"
