def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var my_list = {
        "unused": "value",
    }
    process(List([List([{"inner": my_list^}])]))
