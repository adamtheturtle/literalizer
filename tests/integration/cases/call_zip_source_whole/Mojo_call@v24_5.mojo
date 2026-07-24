def process(value: Int) -> None:
    pass
def emit[*Ts: AnyType](*args: *Ts):
    pass
def main():
    emit(process(42), "one")
