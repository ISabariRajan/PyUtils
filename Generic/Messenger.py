"""
Author      - Sabari                           
Module module	- Messenger                                           
Version     - 1.0											                          	 
Description	- This is custom python module contains data object    
                which can be used in various operations including   
                inter-process communication                     
"""
class Messenger:
  """Messenger - A customised class which holds details for inter-process communication
  """

  module = ""

  def __init__(self, data = {}, message = "", status = "", level = "", module = "", fun_name = ""):
    self.data = data
    self.message = message
    self.status = status
    self.level = level
    self.module = module
    self.fun_name = fun_name
  

  def __str__(self):
    return "Data: " + str(self.data) + "\n" + \
    "Message: " + str(self.message) + "\n" + \
    "Status: " + str(self.status) + "\n" + \
    "Level: " + str(self.level) + "\n" + \
    "Module: " + str(self.module) + "\n"


class JSONList(object):
  """JSONList - A custom class, which convert python list/ tuple object into a collection of __dict__ object and
      store it in 'list' variable
  """
  def __init__(self, list_value = None):
    output = []
    for data in list_value:
      output.append(data.__dict__)
    self.list		= output
    return  None

def object_to_json(object = None):
  """object_to_json -  This function converts an object into __dict__ object which in turn can be used as JSON

  Arguments:
    object {object} -- Any valid python object

  Returns:
    __dict__ -- The dictionary value of python object or None if the object is not valid
  """
  if(not object):
    return None
  if(isinstance(object, list) or isinstance(object, tuple)):
    object		= JSONList(object)
  return object.__dict__
