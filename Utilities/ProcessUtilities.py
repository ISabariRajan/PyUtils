from .package import Utilities, subprocess, CustomError, logger

# Contains Process/ Subprocess related Functions
class ProcessUtilities(Utilities):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # botname = kwargs["botname"]
        # if botname:
        # else:
        #     super().__init__(botname=logger.__get_bot_name__(__file__), **kwargs)
        self.print_debug_log(f"Initialized {self.__class__}")

    def run_process(self, process_list, stream=False):
        header = "run_process: "
        self.print_info_log(header + str(process_list))
        process = subprocess.Popen(process_list[0],
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        
        outputs = []
        errors = []
        if(stream):
            self.print_info_log(header + "Stream start")
            while True:
                # self.print_info_log(process.stdout.readline())
                output = self.decode(process.stdout.readline())
                outputs.append(output)
                errorline = self.decode(process.stderr.readline())
                errors.append(errorline)
                if((errorline) and ("SSHelper" not in errorline)):
                    if "Connection refused" in errorline:
                        raise CustomError(1)
                    if "closed" in errorline:
                        raise CustomError(1)
                    else:
                        self.print_info_log("Error: " + errorline)
                if (output == '') and (process.poll() is not None) and (errorline == ''):
                    break
                if output:
                    self.print_info_log(header + output)
                    # self.print_info_log(header + output.strip())
            self.print_info_log(header + "Stream End")
            #rc = process.poll()
            return outputs, errors
        return process.communicate()
