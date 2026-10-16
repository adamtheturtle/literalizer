class Make_widget_ {
    construct new() {}
    call(count) {}
}
var make_widget = Make_widget_.new()
var my_data = make_widget.call(42)
make_widget.call(my_data)
my_data = make_widget.call(my_data)
// note
make_widget.call(my_data)
