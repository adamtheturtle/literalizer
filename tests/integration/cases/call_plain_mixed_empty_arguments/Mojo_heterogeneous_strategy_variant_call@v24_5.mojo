from std.utils.variant import Variant
comptime Value = Variant[String, Int, List[Int], List[String]]
def make_widget[*Ts: Movable](var *args: *Ts) -> None:
    pass
def main():
    make_widget(List[String](), List([Value(1)]), List[String]())
    make_widget(List([Value(String("text"))]), List([Value(2)]), List[String]())
    make_widget(List[String](), List([Value(String("text"))]), List[String]())
    make_widget(List([Value(String("text"))]), List([Value(2)]), List([Value(3)]))
