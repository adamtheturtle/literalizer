module Main

type ThingType_() =
    member _.Before(_value: obj) : obj = null
let thing = ThingType_()
type Val =
    | FInt of int64
thing.Before(FInt 1L) |> ignore
