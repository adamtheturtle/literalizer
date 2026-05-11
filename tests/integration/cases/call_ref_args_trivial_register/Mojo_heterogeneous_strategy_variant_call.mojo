from std.utils.variant import Variant
comptime Value = Variant[Bool, Int, Float64]
def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var my_int = 1
    var my_bool = True
    var my_float = 3.14
    var my_list = [
        1,
        2,
        3,
    ]
    process(my_int, 42)
    process(my_bool, 7)
    process(my_float, 9)
    process(my_list^, 1)
