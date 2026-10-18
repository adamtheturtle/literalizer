def f(value: List[List[Int]]):
    pass
def main():
    var ref_data = List([
        1,
        2,
    ])
    f(List([
        ref_data.copy(),
    ]))
    f(List([
        ref_data.copy(),
    ]))
