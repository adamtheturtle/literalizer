class Process_ {
    construct new() {}
    call(data, count) {}
}
var process = Process_.new()
var shared = 1
var other = 2
process.call(shared, 1)
process.call(other, 0)
process.call(shared, 8)
