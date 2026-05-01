fn send[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var existing = 42
    send(existing)
