module Check

type Val =
    | FInt of int64
let mutable my_data: Val = FInt 42  // noteL
