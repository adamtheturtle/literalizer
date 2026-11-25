module Main

type Val =
    | FStr of string
    | FList of Val list
let ``process`` (_value: obj) : obj = null
// Test cases
``process``(FStr "hello") |> ignore  // single word
``process``(FStr "hello world") |> ignore  // two words
// trailing comment
