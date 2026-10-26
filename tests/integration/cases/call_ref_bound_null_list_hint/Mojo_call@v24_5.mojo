def consume[*Ts: Movable](var *args: *Ts):
    pass
def main():
    var item = None
    consume(item)
