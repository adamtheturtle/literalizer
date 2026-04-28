class Process_ {
    call(value) {}
}
var process = Process_.new()
process.call("hello")
process.call(42)
process.call(true)
