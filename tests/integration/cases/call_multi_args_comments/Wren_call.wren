class Process_ {
    construct new() {}
    call(ts, start, end) {}
}
var process = Process_.new()
process.call(1, 0, 3600)  // Jan 1 1970 00:00:00 - 01:00:00
process.call(5, 0, 3600)  // Jan 1 1970 00:00:05 - 01:00:05
process.call(2, 0, 5400)  // Jan 1 1970 00:00:02 - 01:30:02
