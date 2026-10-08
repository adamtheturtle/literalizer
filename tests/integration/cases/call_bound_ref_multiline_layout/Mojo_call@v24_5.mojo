def f(value: List[List[List[List[Int]]]]):
    pass
def main():
    var ref_data = List([
        List([
            1,
            2,
        ]),
        List([
            3,
            4,
        ]),
    ])
    f(List([
        List([
            ref_data.copy(),
        ]),
    ]))
