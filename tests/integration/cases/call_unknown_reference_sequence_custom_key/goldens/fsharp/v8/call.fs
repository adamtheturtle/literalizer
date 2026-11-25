module Main

type Val =
    | FList of Val list
let ``process`` (_data: obj) : obj = null
let untypedValue: Val = FList []
``process``(FList [untypedValue; untypedValue]) |> ignore
