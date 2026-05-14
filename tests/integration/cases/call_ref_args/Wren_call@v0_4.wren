class Process_ {
    construct new() {}
    call(data, count) {}
}
var process = Process_.new()
var my_var = [
    1,
    2,
    3,
]
var my_other = [
    4,
    5,
    6,
]
process.call(my_var, 42)
process.call(my_other, 7)
