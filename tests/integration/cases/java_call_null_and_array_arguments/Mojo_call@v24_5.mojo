def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    process(None)
    process(List([1, 2]))
