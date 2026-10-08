module Main

let process (_value: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
process(FInt 1L)  // note<U+2028>still commented<U+2029>done
