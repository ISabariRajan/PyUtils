# from . import package
from Utilities.package import ProcessUtilities, subprocess, logger
class WindowsProcessUtilities(ProcessUtilities):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # botname = kwargs["botname"]
        # if botname:
        # else:
        #     super().__init__(botname=logger.__get_bot_name__(__file__), **kwargs)
        self.print_debug_log(f"Initialized {self.__class__}")

    def find_task_details_pid_from_windowtitlename(self, window_title):
        self.messenger.fun_name = "find_task_details_pid_from_windowtitlename"
        p = 'tasklist /v | findstr /c:"' + window_title + '"'
        process = subprocess.Popen(p,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        lines = process.stdout.readlines()
        if len(lines) < 1:
            return []
        if "No tasks are running which match the specified criteria" in self.decode(lines[0]):
            # self.messenger.message = window_title + " is not here/ Quitting the Job"
            self.print_info_log(window_title + " is not here/ Quitting the Job")
            return None
        for line in lines:
            line = self.decode(line)
            if window_title.lower() in line.lower():
                pid = line.split()
        return pid

    def check_and_kill_process(self, process_name):
        self.messenger.fun_name = "check_and_kill_process"
        self.print_info_log("Check and kills: " + process_name)
        process_details = self.find_task_details_pid_from_windowtitlename(process_name)
        if(len(process_details) > 0):
            process_details = process_details[0]
            if process_details != None:
                self.print_info_log("Killing Running Process: " + process_name)
                p = "wmic process where " + '"name=' + "'" + process_details + "'" + '" delete'
                self.run_process([p])
            else:
                self.print_info_log(process_name + " is not running")
