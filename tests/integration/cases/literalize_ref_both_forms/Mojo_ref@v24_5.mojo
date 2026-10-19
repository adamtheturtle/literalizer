def main():
    var shared_values = List([
        1,
        2,
    ])
    var my_data = {
        "a": shared_values.copy(),
    }
    _ = my_data
    my_data = {
        "a": shared_values.copy(),
    }
    _ = my_data
