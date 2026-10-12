module Main

let f (_a: obj) : obj = null
type Val =
    | FList of Val list
f(FList [])
