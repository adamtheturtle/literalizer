class Process_ {
    construct new() {}
    call(data) {}
}
var process = Process_.new()
var my_list = {
    "unused": "value",
}
process.call([[{"inner": my_list}]])
