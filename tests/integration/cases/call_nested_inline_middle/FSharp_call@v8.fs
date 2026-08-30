module Main

type Val =
    | FStr of string
    | FList of Val list
let f (_ops: obj) : obj = null
f(FList [FList [FStr "DEL"; FStr "b"; FStr "10"]; FList [FStr "ADD"; FStr "a"; FStr "x"]])  // note
// next call
f(FList [FList [FStr "ADD"; FStr "c"; FStr "y"]])
