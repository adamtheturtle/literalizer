class Process_ {
    construct new() {}
    call(data, count) {}
}
var process = Process_.new()
var single_var = [
    4,
    5,
    6,
]
var repeated_var = 1
process.call(repeated_var, 1)
process.call(single_var, 0)
process.call(repeated_var, 8)
