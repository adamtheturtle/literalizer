class Make_widget_ {
    construct new() {}
    call(count) {}
}
var make_widget = Make_widget_.new()
var my_data = (`__LINE__ > 0) ? make_widget.call(42) : make_widget.call(42) // trailing `marker
