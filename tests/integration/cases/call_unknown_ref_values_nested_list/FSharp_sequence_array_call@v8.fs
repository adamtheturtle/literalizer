module Main

type Val =
    | FList of Val array
let ``process`` (_data: obj) : obj = null
let unknown_value: Val array = [||]
``process``([|unknown_value|]) |> ignore
