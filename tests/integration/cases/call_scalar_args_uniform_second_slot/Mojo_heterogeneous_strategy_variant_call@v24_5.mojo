from std.utils.variant import Variant
comptime Value = Variant[String, Int, Bool]
def process(value: Value, label: String):
    pass
def main():
    process(Value(String("hello")), "a")
    process(Value(42), "b")
    process(Value(True), "c")
