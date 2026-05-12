from std.utils.variant import Variant
comptime Value = Variant[NoneType, String]
def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    process(Value(NoneType()))
    process(Value(String("hello")))
