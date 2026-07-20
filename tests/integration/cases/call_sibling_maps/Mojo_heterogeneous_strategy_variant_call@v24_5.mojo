from std.utils.variant import Variant
comptime Value = Variant[Int, String, Dict[String, Int], Dict[String, String]]
def process(value: Dict[String, Value]):
    pass
def main():
    process({"value": Value(1)})
    process({"value": Value(String("hello"))})
