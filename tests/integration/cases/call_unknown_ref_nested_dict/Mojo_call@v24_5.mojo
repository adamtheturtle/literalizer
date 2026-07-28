def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var my_list = List[String]()
    process([[{"inner": my_list}]])
