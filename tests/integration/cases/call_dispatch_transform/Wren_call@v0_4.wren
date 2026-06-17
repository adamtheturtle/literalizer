class Record_ {
    construct new() {}
    call(value) {}
}
var record = Record_.new()
class Flush_ {
    call(count) {}
var flush = Flush_.new()
record.call(42)
flush.call(3)
