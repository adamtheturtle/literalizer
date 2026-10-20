def make_widget[*Ts: AnyType](*args: *Ts) -> None:
    pass
def main():
    make_widget(List[String](), List([1]), List[String]())
    make_widget(List(["text"]), List([2]), List[String]())
    make_widget(List[String](), List(["text"]), List[String]())
    make_widget(List(["text"]), List([2]), List([3]))
