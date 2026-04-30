fn process[*Ts: AnyType](*args: *Ts):
    pass
fn emit[*Ts: AnyType](*args: *Ts):
    pass
def main():
    emit(process())
    emit(process())
