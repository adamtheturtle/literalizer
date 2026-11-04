module Main

type ThingType_() =
    member _.go(_before: obj, _populated: obj, _after: obj) : obj = null
let thing = ThingType_()
type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
thing.go(FList [], FList [FInt 1L], FList []) |> ignore
thing.go(FList [FStr "text"], FList [FInt 2L], FList []) |> ignore
thing.go(FList [], FList [FStr "text"], FList []) |> ignore
thing.go(FList [FStr "text"], FList [FInt 2L], FList [FInt 3L]) |> ignore
