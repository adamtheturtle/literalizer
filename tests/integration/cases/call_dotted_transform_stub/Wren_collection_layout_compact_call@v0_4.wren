class Process_ {
    construct new() {}
    call(value) {}
}
var process = Process_.new()
class Tracer_ {
    construct new() {}
    emit(arg) {}
}
var tracer = Tracer_.new()
tracer.emit(process.call("hello"))
tracer.emit(process.call(42))
tracer.emit(process.call(true))
