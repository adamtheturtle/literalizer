class Process_ {
    construct new() {}
    call(known_value, nested_missing) {}
}
var process = Process_.new()
var known_value = true
var unknown_value = true
process.call(known_value, [unknown_value])
