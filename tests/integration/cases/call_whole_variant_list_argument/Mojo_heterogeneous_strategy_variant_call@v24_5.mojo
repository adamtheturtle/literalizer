from std.utils.variant import Variant
comptime Value = Variant[Int, String]
def f(var a: List[Value]):
    pass
def main():
    f(List([Value(1), Value(String("x"))]))
