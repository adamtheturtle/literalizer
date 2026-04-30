module Main

type Val =
    | FInt of int64
    | FList of Val list
let process (_ts: obj, _start: obj, _end: obj) : obj = null
process(1, 0, 3600)  // Jan 1 1970 00:00:00 - 01:00:00
process(5, 0, 3600)  // Jan 1 1970 00:00:05 - 01:00:05
process(2, 0, 5400)  // Jan 1 1970 00:00:02 - 01:30:02
