def make_widget[*Ts: AnyType](var *args: *Ts):
    pass
def main():
    make_widget(List[String]())
