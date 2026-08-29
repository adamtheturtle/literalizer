def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var big_list: List[String] = List([
        "x",
    ])
    process(List([Tuple("m", big_list^)]))
