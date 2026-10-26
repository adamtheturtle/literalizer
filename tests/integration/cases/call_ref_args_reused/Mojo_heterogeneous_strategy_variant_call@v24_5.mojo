from std.utils.variant import Variant
comptime Value = Variant[Int, List[Int]]
def process(var data: Value, var count: Int):
    pass
def main():
    var single_var = List([
        4,
        5,
        6,
    ])
    var repeated_var = 1
    process(repeated_var, 1)
    process(single_var^, 0)
    process(repeated_var, 8)
