def main():
    var shared = List([
        1,
        2,
    ])
    var my_data = List([
        {"left": shared.copy(), "right": shared.copy()},
    ])
    _ = my_data
