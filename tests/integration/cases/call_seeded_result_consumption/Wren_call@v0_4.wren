class Make_widget_ {
    construct new() {}
    call(count) {}
}
var make_widget = Make_widget_.new()
class Consume_widget_ {
    construct new() {}
    call(count) {}
}
var consume_widget = Consume_widget_.new()
var my_data = make_widget.call(0)
consume_widget.call(my_data)
my_data = make_widget.call(1)
consume_widget.call(my_data)
