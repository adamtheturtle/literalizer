def f[*Ts: AnyType](*args: *Ts):
    pass
def main():
    f(List([1, 2]))
