class Process_ {
    construct new() {}
    call(data) {}
}
var process = Process_.new()
var my_var = 42
var my_other = 7
process.call([my_var, 42, "static"])
process.call([my_other, 7, "label"])
