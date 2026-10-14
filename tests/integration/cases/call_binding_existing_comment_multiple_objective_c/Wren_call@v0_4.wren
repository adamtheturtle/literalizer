class Make_widget_ {
    construct new() {}
    call(count) {}
}
var make_widget = Make_widget_.new()
var my_data = make_widget.call(42)
my_data = make_widget.call(my_data) // note
// extra
make_widget.call(my_data)
