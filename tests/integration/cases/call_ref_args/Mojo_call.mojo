def main():
    def process(*args: object) -> object: return object()
    var my_var = [
        1,
        2,
        3,
    ]
    var my_other = [
        4,
        5,
        6,
    ]
    process(my_var, 42)
    process(my_other, 7)
