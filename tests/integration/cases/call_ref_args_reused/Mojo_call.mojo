fn process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var shared = 1
    var other = 2
    process(shared, 1)
    process(other^, 0)
    process(shared, 8)
