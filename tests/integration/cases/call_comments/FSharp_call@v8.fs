module Main

type Val =
    | FStr of string
    | FList of Val list
let process (_value: obj) : obj = null
// Test cases
process(FStr "hello")  // single word
process(FStr "hello world")  // two words
// trailing comment
