class Process_ {
    construct new() {}
    call(value, label) {}
}
var process = Process_.new()
process.call("hello", "a")
process.call(42, "b")
process.call(true, "c")
