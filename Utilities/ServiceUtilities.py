from .package import ProcessUtilities, logger


class ServiceUtilities(ProcessUtilities):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # botname = kwargs["botname"]
        # if botname:
        # else:
        #     super().__init__(botname=logger.__get_bot_name__(__file__), **kwargs)
        self.print_debug_log(f"Initialized {self.__class__}")


    # Service and Packages
    def restart_service(self, service_name, stream=True):
        return self.run_process(["systemctl restart " + service_name], stream)
    
    def start_service(self, service_name, stream=True):
        return self.run_process(["systemctl start " + service_name], stream)
    
    def stop_service(self, service_name, stream=True):
        return self.run_process(["systemctl stop " + service_name], stream)

    def status_service(self, service_name, stream=True):
        return self.run_process(["systemctl status " + service_name], stream)
    
    def install_from_repo(self, package_name, stream=True):
        return self.run_process(["apt-get -y install " + package_name], stream)

