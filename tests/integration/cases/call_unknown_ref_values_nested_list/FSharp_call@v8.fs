module Main

type Val =
    | FList of Val list
let process (_data: obj) : obj = null
let unknown_value: Val = FList []
process(FList [unknown_value])
