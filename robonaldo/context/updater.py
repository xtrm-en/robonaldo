try:
    import rsk2 as rsk
except:
    import rsk

class ContextUpdater():
    def __init__(self, host: str, key: str = ""):
        self.__host = host
        self.__key = key

        self.__client = rsk.Client(host = host, key = key)
        self.__client.on_update = lambda cl, dt: self.dispatch_context(cl, dt)

        self.__ctx = None
        
        self.__audience = []
        

    def dispatch_context(self, client: rsk.Client, deltaTime: float):
        self.update_context(client, deltaTime)

        for listener in self.__audience:
            listener(self.__ctx, deltaTime)
        
    def update_context(self, client: rsk.Client, deltaTime: float):
        pass

