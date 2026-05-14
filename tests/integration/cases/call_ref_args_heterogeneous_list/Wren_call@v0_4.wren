class Process_ {
    construct new() {}
    call(data, count) {}
}
var process = Process_.new()
var my_ints = [
    1,
    2,
    3,
]
var my_strings = [
    "a",
    "b",
]
var my_empty = []
process.call(my_ints, 42)
process.call(my_strings, 7)
process.call(my_empty, 99)
