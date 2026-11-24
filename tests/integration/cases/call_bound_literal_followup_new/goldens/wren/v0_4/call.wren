class Make_widget_ {
    construct new() {}
    call(value) {}
}
var make_widget = Make_widget_.new()
class Consume_ {
    construct new() {}
    call(value) {}
}
var consume = Consume_.new()
var my_data = make_widget.call(42)
consume.call(my_data)
