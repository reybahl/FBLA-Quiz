"""FBLA Singleton
.. moduleauthor:: Reyansh Bahl <https://github.com/reybahl>
"""

class Singleton:
    """This is a singleton file used as a decorator for :class:`Connection`
    so as to disable creation of multiple instances of the :class:`Connection` object.
    We do not need to create the instance again and again and this helps in saving memory
    and time of database connection object.
    """
    def __init__(self, cls):
        """init method
        
        :param cls: The class on which the decorator is placed.
        :type cls: class
        """
        self._cls = cls

    def Instance(self):
        """Creates a single instance. If there's already an instance, it returns
        that instance.
        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        """Gets called if someone tries to create an instance and throws error
        because that's not allowed as we want to create a single instance.
        """
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        """Checks if the instance is of the type cls.
        
        :param inst: The class on which the decorator is placed.
        :type inst: class
        """
        return isinstance(inst, self._cls)
