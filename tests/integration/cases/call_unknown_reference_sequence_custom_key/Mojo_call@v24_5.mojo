def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var untyped_value = List[String]()
    process(List([untyped_value, untyped_value]))
