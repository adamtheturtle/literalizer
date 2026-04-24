alias Value = Variant[Int, String]
def main():
    var my_data = {
        "a": Value(1),
        "b": Value(String("x")),
    }
    _ = my_data
    my_data = {
        "a": Value(1),
        "b": Value(String("x")),
    }
    _ = my_data
