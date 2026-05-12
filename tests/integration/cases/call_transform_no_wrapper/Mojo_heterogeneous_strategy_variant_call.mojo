from std.utils.variant import Variant
comptime Value = Variant[String, Int, Bool]
def process(value: Value) -> object:
    pass
def main():
    process(Value(String("hello")))
    process(Value(42))
    process(Value(True))
