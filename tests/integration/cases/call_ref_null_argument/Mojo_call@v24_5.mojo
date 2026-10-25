def consume[*Ts: AnyType](var *args: *Ts):
    pass
def main():
    var value = None
    consume(value)
