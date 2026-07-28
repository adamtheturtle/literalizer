def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var known_value = 1
    var unknown_value = List[String]()
    process(unknown_value)
