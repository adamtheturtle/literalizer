class Process_ {
    construct new() {}
    call(value, count) {}
}
var process = Process_.new()
var my_int = 1
var my_bool = true
var my_float = 3.14
var my_list = [
    1,
    2,
    3,
]
process.call(my_int, 42)
process.call(my_bool, 7)
process.call(my_float, 9)
process.call(my_list, 1)
