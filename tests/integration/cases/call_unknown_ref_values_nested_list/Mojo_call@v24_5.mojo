def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var unknown_value = List[String]()
    process([unknown_value])
