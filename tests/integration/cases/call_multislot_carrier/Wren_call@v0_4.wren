class Process_ {
    construct new() {}
    call(value, extra) {}
}
var process = Process_.new()
process.call(1, "hello")
process.call("two", false)
process.call(3.5, null)
