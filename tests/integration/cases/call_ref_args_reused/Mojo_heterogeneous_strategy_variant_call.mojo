def process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var single_var = [
        4,
        5,
        6,
    ]
    var repeated_var = 1
    process(repeated_var, 1)
    process(single_var^, 0)
    process(repeated_var, 8)
