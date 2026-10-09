def consume[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var my_null = None
    var regular_null = None
    consume(my_null^)
    consume(regular_null)
