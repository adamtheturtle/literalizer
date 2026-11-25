class Process_ {
    construct new() {}
    call(value) {}
}
var process = Process_.new()
class Helpers_ {
    construct new() {}
    emit(argument0, argument1) {}
}
var helpers = Helpers_.new()
helpers.emit(process.call(1), 42)
