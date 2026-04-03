module Check

type Val =
    | FInt of int64
// note
let mutable my_data: Val = FInt 42L
