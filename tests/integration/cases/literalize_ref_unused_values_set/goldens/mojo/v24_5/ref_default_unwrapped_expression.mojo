from std.collections import Set
def consume_widget[*Ts: Movable](var *args: *Ts):
    pass
def main():
    consume_widget(Set[Int](
        1,
        2,
    ))
