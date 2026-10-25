def process(var value: Int) -> None:
    pass
def emit[*Ts: AnyType](var *args: *Ts):
    pass
def main():
    emit(process(1), 42)
