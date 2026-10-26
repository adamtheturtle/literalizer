class Make_widget_ {
    construct new() {}
    call(first, second) {}
}
var make_widget = Make_widget_.new()
class Consume_ {
    construct new() {}
    call(first, second) {}
}
var consume = Consume_.new()
var my_data = make_widget.call(42, 3)
consume.call(my_data, 3)
