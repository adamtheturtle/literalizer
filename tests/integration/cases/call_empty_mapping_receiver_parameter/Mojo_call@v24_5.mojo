@fieldwise_init
struct _ApiType(Copyable, Movable):
    def process[*Ts: Movable](self, var *args: *Ts):
        pass
def main():
    var api = _ApiType()
    api.process(Dict[String, String]())
