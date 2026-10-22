def consume[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var item = List([
        1,
        2,
    ])
    consume(item^)
