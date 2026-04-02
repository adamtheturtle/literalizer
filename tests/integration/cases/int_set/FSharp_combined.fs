module Check

type Val =
    | FInt of int64
    | FSet of Val list
let mutable my_data: Val = FSet [
    FInt 1L;
    FInt 2L;
    FInt 3L
]
