module Main

type Val =
    | FInt of int64
    | FList of Val list
let consume (_value: obj) : obj = null
let external_value: Val = FInt 1L
consume(external_value)
