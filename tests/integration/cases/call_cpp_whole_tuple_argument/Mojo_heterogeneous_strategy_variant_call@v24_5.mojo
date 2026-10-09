from std.utils.variant import Variant
comptime Value = Variant[String, Int, Bool]
def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    process(List([Value(String("hello")), Value(42), Value(True)]))
