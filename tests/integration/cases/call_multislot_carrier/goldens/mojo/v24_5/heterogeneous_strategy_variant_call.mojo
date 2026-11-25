from std.utils.variant import Variant
comptime Value = Variant[Int, String, Bool, Float64, NoneType]
def process(var value: Value, var extra: Value):
    pass
def main():
    process(Value(1), Value(String("hello")))
    process(Value(String("two")), Value(False))
    process(Value(Float64(3.5)), Value(NoneType()))
