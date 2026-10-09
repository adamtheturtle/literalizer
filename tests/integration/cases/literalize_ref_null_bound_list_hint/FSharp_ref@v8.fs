module Main

type Val =
    | FNull
    | FInt of int64
    | FList of Val list
let myValue: Val = FNull
let my_data: Val = myValue
