module Main

type Val =
    | FList of Val array
let ``process`` (_data: obj) : obj = null
let untypedValue: Val array = [||]
``process``([|untypedValue; untypedValue|]) |> ignore
