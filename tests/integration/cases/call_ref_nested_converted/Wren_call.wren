class Process_ {
    construct new() {}
    call(data) {}
}
var process = Process_.new()
var my_var = 42
process.call([{"ref": "myVar"}, 42, "static"])
