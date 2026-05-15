class Process_ {
    construct new() {}
    call() {}
}
var process = Process_.new()
class Emit_ {
    construct new() {}
    call(arg) {}
}
var emit = Emit_.new()
emit(process.call())
emit(process.call())
