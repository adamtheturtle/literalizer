module Check

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
let process (a: obj) : obj = a
process("hello")
process(42)
process(FBool true)
