from std.utils.variant import Variant
comptime Value = Variant[Int, String]
def make_widget(first_value: List[Value], second_value: List[Value]):
    pass
def main():
    make_widget(List([Value(1)]), List([Value(String("text"))]))
