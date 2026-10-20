def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var item = List([
        1,
        2,
    ])
    process(item.copy())
    process(item.copy())
