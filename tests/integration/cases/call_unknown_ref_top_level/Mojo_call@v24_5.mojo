def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var unknown_value = List([
        1,
    ])
    process(unknown_value)
