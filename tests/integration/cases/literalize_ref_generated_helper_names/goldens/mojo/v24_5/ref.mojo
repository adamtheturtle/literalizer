def main():
    var std = {
        "a": 1,
    }
    var arena = {
        "a": 1,
    }
    var allocator = {
        "a": 1,
    }
    var my_data = List([
        std.copy(),
        arena.copy(),
        allocator.copy(),
    ])
    _ = my_data
