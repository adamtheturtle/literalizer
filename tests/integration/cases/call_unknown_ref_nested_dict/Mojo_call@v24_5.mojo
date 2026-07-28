def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var my_list = {
        "unused": "value",
    }
    process([[{"inner": my_list^}]])
