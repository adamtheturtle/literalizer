module Main

let DoThing (_x: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
DoThing(FInt 1L)
DoThing(FInt 2L)
