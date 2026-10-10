from std.utils.variant import Variant
comptime Value = Variant[Int, String]
def f[*Ts: AnyType](*args: *Ts):
    pass
def main():
    f(List([Value(1), Value(String("x"))]))
