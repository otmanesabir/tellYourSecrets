import yaml
import os

class global_config:
    """
    a Singleton class to serve the GlobalValues
    USAGE: (FirstTime)
    from myClasses.globals import GlobalValues
    global_values = GlobalValues()
    global_values.<new value> = ...
    ... = global_values.<value>
    USAGE: (Second and n'th time, in same module or other modules)
        NB adjust `from myClasses.globals` dependent on relative path to this module 
    from myClasses.globals import GlobalValues 
    global_values = GlobalValues.getInstance()
    global_values.<new value> = ...
    ... = global_values.<value>
    """

    def __load_config():
        #Add a new global value:
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        cfg = None
        f = open(os.path.join(__location__, 'config.yaml'))
        try:
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            print(e)
        return cfg

    __instance = None
    CFG = __load_config()

    @staticmethod
    def get_instance():
        """ Static access method. """
        if global_config.__instance == None:
            global_config()
        return global_config.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if global_config.__instance != None:
            raise Exception("This class is a singleton! once created use global_values = Glovalvalues.get_instance()")
        else:
            global_config.__instance = self
