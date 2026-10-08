def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var unknown_value = List[String]()
    process(List([unknown_value]))
