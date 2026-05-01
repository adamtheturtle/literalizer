fn process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var existing = 42
    process(existing)
