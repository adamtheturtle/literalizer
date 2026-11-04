module Main

type ThingType_() =
    member _.go(_before: obj, _populated: obj, _after: obj) : obj = null
let thing = ThingType_()
type Val =
    | FInt of int64
    | FStr of string
    | FList of Val array
thing.go([||], [|FInt 1L|], [||]) |> ignore
thing.go([|FStr "text"|], [|FInt 2L|], [||]) |> ignore
thing.go([||], [|FStr "text"|], [||]) |> ignore
thing.go([|FStr "text"|], [|FInt 2L|], [|FInt 3L|]) |> ignore
