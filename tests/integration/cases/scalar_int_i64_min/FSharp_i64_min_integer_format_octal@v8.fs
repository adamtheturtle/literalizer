module Main

type Val =
    | FInt of int64
let my_data: Val = FInt(-0o1000000000000000000000L)
