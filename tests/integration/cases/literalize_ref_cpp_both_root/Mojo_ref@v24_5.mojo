def main():
    var shared = List([
        1,
        2,
    ])
    var my_data = shared.copy()
    _ = my_data
    my_data = shared.copy()
    _ = my_data
