def f(a: Int) -> None:
    pass
def repr[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var ref_data = 1
    repr(f(ref_data))
