module Main

type Val =
    | FInt of int64
    | FList of Val list
type ThingType_() =
    member _.go(_value: obj) : obj = null
let thing = ThingType_()
let item: Val = FList [
    FInt 1L;
    FInt 2L
]
thing.go(item)
