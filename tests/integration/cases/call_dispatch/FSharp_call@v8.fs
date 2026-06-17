module Main

let put (_key: obj, _value: obj) : obj = null
let get (_key: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
put(1, 10)
get(1)
