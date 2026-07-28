def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var known_value = True
    var unknown_value = True
    process(known_value, unknown_value)
