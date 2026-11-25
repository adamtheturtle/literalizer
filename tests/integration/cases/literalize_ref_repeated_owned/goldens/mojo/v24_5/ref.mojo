def main():
    var shared = List([
        1,
        2,
    ])
    var my_data = List([
        shared.copy(),
        shared.copy(),
    ])
    _ = my_data
