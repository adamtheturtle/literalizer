module Main

type Val =
    | FStr of string
    | FList of Val list
let process (_value: obj) : obj = null
// Test cases
process("hello")  // single word
process("hello world")  // two words
// trailing comment
