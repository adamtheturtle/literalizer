class Process_ {
    construct new() {}
    call(data) {}
}
var process = Process_.new()
var my_var = 42
process.call({"key": {"ref": "my_var"}, "count": 42})
