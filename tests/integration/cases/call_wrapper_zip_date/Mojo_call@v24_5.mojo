def process(var value: Int) -> None:
    pass
def emit[*Ts: Movable](var *args: *Ts):
    pass
def main():
    emit(process(1), "2024-01-15")
