module Main

type Val =
    | FInt of int64
let stamp: Val = FInt 1L
let result_data: Val = stamp
