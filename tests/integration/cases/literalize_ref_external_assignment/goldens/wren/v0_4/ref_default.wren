class Consume_widget_ {
    construct new() {}
    call(arg_value) {}
}
var consume_widget = Consume_widget_.new()
var ref_data = [
    1,
    2,
]
var my_data = [
    0,
]
consume_widget.call(my_data)
my_data = ref_data
consume_widget.call(my_data)
