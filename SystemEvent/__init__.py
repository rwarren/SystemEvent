import posix_ipc  # TODO: eliminate this dependency (with ctypes)

class SystemEvent(object):
    def __init__(self, name, prefix = "SystemEvent."):
        """Inter-process Event object that follows threading.Event semantics.
        
        This uses a posix semaphore under the hood, and the name parameter will be the
        name of the semaphore. This must be unique, but known to other processes that
        want to use the SystemEvent/semaphore.
        
        Note that any incrementing/releasing of the underlying semaphore will effectively
        set the SystemEvent.
        
        """
        self._name = prefix + name
        self._sem = posix_ipc.Semaphore(self._name, flags = posix_ipc.O_CREAT)
    
    def set(self):
        """Sets the event as having occurred.
    
        All processes waiting for the event to be set are awakened. Processes that call
        wait() once the event is set will not block at all.
    
        """
        self._sem.release()
    
    def clear(self):
        """Reset the event.
        
        Subsequently, SystemEvent instances calling wait() will block until set() is
        called to set the event again.
    
        """        
        # The semaphore *should* only ever get to 1, but we'll fully clear it out, just
        # in case other process meddling isn't implemented quite correctly.
        while True:
            try:
                self._sem.acquire(0)
            except posix_ipc.BusyError:
                break
    
    def wait(self, timeout = None):
        """Block until the event is set.
        
        If the event is already set on entry, return immediately. Otherwise, block until
        the event is set, or until the optional timeout occurs.
        
        When the timeout argument is present and not None, it should be a floating point
        number specifying a timeout for the operation in seconds (or fractions thereof).
        
        This method returns a boolean indicating if the event is set, so it will always
        return True except if a timeout is given and the operation times out.
        
        """
        try:
            self._sem.acquire(timeout)
        except posix_ipc.BusyError:
            return False
        # Need to release it immediately so that other SystemEvents can acquire it...
        self._sem.release()
        return True
    
    def isSet(self):
        """Return true if and only if the event is set at the time of the call."""
        return self.wait(0)
