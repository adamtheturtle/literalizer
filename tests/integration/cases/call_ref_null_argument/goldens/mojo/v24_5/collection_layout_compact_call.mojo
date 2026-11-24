def consume[*Ts: Movable](var *args: *Ts):
    pass
def main():
    var value = None
    consume(value)
