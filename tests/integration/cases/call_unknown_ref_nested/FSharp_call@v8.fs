module Main

type Val =
    | FBool of bool
    | FList of Val list
let process (_known_value: obj, _nested_missing: obj) : obj = null
let known_value: Val = FBool true
let unknown_value: Val = FBool true
process(known_value, unknown_value)
