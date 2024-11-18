from . import os, shutil, json
from .package import ProcessUtilities, logger

# Contains File related functions
class FileUtilities(ProcessUtilities):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # botname = kwargs["botname"]
        # if botname:
        # else:
        #     super().__init__(botname=logger.__get_bot_name__(__file__), **kwargs)
        self.print_debug_log(f"Initialized {self.__class__}")


    def take_ownership(self, full_path, group=None, user=None, is_recursive=False):
        command = "sudo chown -R x:x folder"
        ug = ":"
        r = " "
        if(group):
            ug = ug + group
        if(user):
            ug = user + ug
        if(is_recursive):
            r = " -R "
        command = "sudo chown " + ug + r + full_path
        self.run_process([command], False)

    def set_file_permission(self, filepath=None, permission=None):
        return

    def clear_directory(self, directory_path):
        self.log("Clearing Directory: " + directory_path)
        file_list = os.listdir(directory_path)
        for current_file in file_list:
            file_full_path = os.path.join(directory_path, current_file)
            if(os.path.isdir(file_full_path)):
                shutil.rmtree(os.path.join(directory_path, current_file))
            elif(os.path.isfile(file_full_path)):
                os.remove(file_full_path)

    def read_json_from_file(self, file_location):
        header = "read_json_from_file: "
        self.log(header + str(file_location))
        data = {}
        try:
            with open(file_location, "r") as f:
                try:
                    data = json.load(f)
                except Exception as e:
                    self.log(header + "Exception: " + str(e))
        except Exception as e:
            self.log(header + "Exception: " + str(e))

        return data

    def write_json_to_file(self, json_value, file_location):
        self.log("write_json_to_file: " + str(file_location))
        with open(file_location, "w+") as f:
            f.write(self.json_to_string(json_value))

    def write_array_to_file(self, filename, values):
        try:
            with open(filename, "w") as f:
                f.writelines(values)
        except:
            return False

        return True
        
    def read_file_as_array(self, filename):
        values = []
        with open(filename, "r") as f:
            values = f.readlines()
        
        return values
    
    # def read_json_from_file(self, file_path):
    #     with open(file_path, "r") as f:
    #         try:
    #             return json.loads(
    #                 "".join(f.readlines())
    #             )
    #         except:
    #             return None
    
    def json_to_string(self, json_value, indent=2):
        return json.dumps(json_value, indent=indent)

    def string_to_json(self, string_value, indent=2):
        return json.loads(string_value)

    def byte_to_json(self, byte, indent=2):
        string_value = self.decode(byte)
        return self.string_to_json(string_value, indent=indent)

    def is_file(self, file_path):
        o,e = self.run_process(["cd '" + file_path + "'"], False)
        if(e):
            return True

        return False

    def get_folder_and_file_list(self, directory_path):
        dir_file_list = os.listdir(directory_path)
        dir_list = []
        file_list = []

        for current_file in dir_file_list:
            file_path = os.path.join(directory_path, current_file)
            if(self.is_file(file_path)):
                file_list.append(current_file)
            else:
                dir_list.append(current_file)
 
        return {
            "dir_list": dir_list,
            "file_list": file_list
        }

    def get_file_list_from_dir(self, directory_path, recursive=False):
        file_list = os.listdir(directory_path)
        full_file_list = []
        all_files = []
        # If recursive loop through all folders in the main directory
        if(recursive):
            for current_file in file_list:
                file_path = os.path.join(directory_path, current_file)
                o,e = self.run_process(["cd " + file_path], False)
                if(self.is_file(file_path)):
                    all_files.append(current_file)
                else:
                    sub_files = self.get_file_list_from_dir(file_path, recursive)
                    full_file_list.extend(sub_files)
            full_file_list.append({
                "name": directory_path,
                "file_list": all_files
            })
            return full_file_list

        # If not recrsive list only the files
        for current_file in file_list:
            file_path = os.path.join(directory_path, current_file)
            o,e = self.run_process(["cd " + file_path], False)
            if(self.is_file(file_path)):
                all_files.append(current_file)
        full_file_list.append({
                "name": directory_path,
                "file_list": all_files
            })
        return full_file_list

    def get_file_path(self, filename):
        return os.path.abspath(filename)
    
    def get_parent_directory(self, filename, directory_hierarcy=1):
        filename = self.get_file_path(filename)
        for i in range(0, directory_hierarcy):
            directory = os.path.dirname(filename)
            filename = directory
        
        return filename
