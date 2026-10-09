module Main

type Val =
    | FInt of int64
    | FList of Val list
let refData: Val = FInt 1L
let my_data: Val = refData
