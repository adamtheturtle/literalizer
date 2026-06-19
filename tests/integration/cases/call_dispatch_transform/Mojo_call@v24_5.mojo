def record_value(value: Int) -> None:
    pass
def flush_buffer(count: Int):
    pass
def emit[*Ts: AnyType](*args: *Ts):
    pass
def main():
    emit(record_value(42))
    flush_buffer(3)
