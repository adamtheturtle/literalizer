module Main

type Val =
    | FInt of int64
    | FBigInt of bigint
let my_data: Val = FBigInt(-9223372036854775809I)
