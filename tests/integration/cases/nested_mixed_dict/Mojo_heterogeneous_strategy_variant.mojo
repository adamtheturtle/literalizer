alias Value = Variant[Int, String, NoneType]
def main():
    var my_data = {
        "outer": {"a": Value(1), "b": Value(String("x")), "c": Value(None)},
    }
    _ = my_data
