class Process_ {
    construct new() {}
    call(data, count) {}
}
var process = Process_.new()
var repeated_var = 1
var single_var = [
    4,
    5,
    6,
]
process.call(repeated_var, 1)
process.call(single_var, 0)
process.call(repeated_var, 8)
