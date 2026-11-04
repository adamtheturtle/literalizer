class Make_widget_ {
    construct new() {}
    call(before, populated, after) {}
}
var make_widget = Make_widget_.new()
make_widget.call([], [1], [])
make_widget.call(["text"], [2], [])
make_widget.call([], ["text"], [])
make_widget.call(["text"], [2], [3])
