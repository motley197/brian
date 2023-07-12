
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
                    
     
def test():
    sens = EnvSensorCapability(has_temp=True, has_pressure=True)
    print(sens.capability)
    sens.set_requirements(["temp"])
    sens.set_requirements(["temp", "humid"])  # Should throw an exception

#test()
