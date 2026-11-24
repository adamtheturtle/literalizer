module Main

let f (_a: obj) : obj = null
type Val =
    | FList of Val array
f([||]) |> ignore
