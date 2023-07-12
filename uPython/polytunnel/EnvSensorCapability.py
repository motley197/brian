####################################################################################################################################
# This is the parent class for all the environmental sensors.
# 
# It plays the following key roles:
# 1 - Allows the capability of a sensor (subclass) to be declared
# 2 - Allows the caller to specify which sensor parameters they wish to use. An exception is raised if the sensor cannot do this
# 
# Having a list of required capabilities allows a concrete subclass to not waste time measuring parameters that are not needed.
# Often some sensors have the same capability. For example:
#     Temperature can often be measured on two different devices.
#     We can now choose which of the sensors performs the temperature measurement
#     We can even mix real sensors with mocked, where the mocked can simulate what is missing in hardware
####################################################################################################################################

class EnvSensorCapability:
     def __init__(self, has_temp:bool=False, has_pressure:bool=False, has_humidity:bool=False, requirements=[]):
          # Capabilities of this sensor
          self.capability = {
               "temp" : has_temp,
               "pres" : has_pressure,
               "humid": has_humidity
          }
          # Set of requirements needed by the calling application - default is none
          self.requirements = {
                "temp"  : False,
                "pres"  : False,
                "humid" : False  
          }
          # Override
          self.set_requirements(requirements)
     
     def __str__(self):
          return f"{self.capability()})"
     
     # The parameter req_list is a list of requirements needed from the calling application. E.g. ["temp", "pres"]
     # An exception will be thrown if the caller requires a parameter this sensor cannot provide
     # This is done so that time is not wasted measuring parameters that are not needed (or replicated elsewhere)
     def set_requirements(self, req_list):
          for key in req_list:
               if (self.capability[key] == False):
                    raise Exception(f'This sensor does not have the capability {key}')
               else:
                    self.requirements[key] = True
                    
     
# ***************************************************************************
# ********************************** Tests ********************************** 
# ***************************************************************************

def test():
    sens = EnvSensorCapability(has_temp=True, has_pressure=True)
    print(sens.capability)
    sens.set_requirements(["temp"])
    sens.set_requirements(["temp", "humid"])  # Should throw an exception

#test()
