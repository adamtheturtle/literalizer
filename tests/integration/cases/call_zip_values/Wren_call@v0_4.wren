class Process_ {
    construct new() {}
    call(value) {}
}
var process = Process_.new()
class Emit_ {
    construct new() {}
    call(call, zip) {}
}
var emit = Emit_.new()
emit(process.call("hello"), true)
emit(process.call(42), false)
