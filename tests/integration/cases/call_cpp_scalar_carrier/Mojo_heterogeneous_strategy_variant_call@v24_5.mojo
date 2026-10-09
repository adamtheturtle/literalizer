from std.utils.variant import Variant
comptime Value = Variant[String, Int, Bool, NoneType]
def process(value: Value):
    pass
def main():
    process(Value(String("hello")))
    process(Value(42))
    process(Value(True))
    process(Value(NoneType()))
