module Main

type ThingType_() =
    member _.first_value(_value: obj) : obj = null
let thing = ThingType_()
type Val =
    | FInt of int64
thing.first_value(FInt 1L) |> ignore
