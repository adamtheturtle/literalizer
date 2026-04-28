module Main

type Val =
    | FInt of bigint
let my_data: Val = FInt(-9223372036854775809I)
