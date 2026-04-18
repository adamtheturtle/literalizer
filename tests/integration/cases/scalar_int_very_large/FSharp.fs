module Check

type Val =
    | FInt of int64
let my_data: Val = FInt 9223372036854775808L
