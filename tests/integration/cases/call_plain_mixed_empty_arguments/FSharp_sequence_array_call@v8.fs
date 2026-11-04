module Main

let make_widget (_before: obj, _populated: obj, _after: obj) : obj = null
type Val =
    | FInt of int64
    | FStr of string
    | FList of Val array
make_widget([||], [|FInt 1L|], [||]) |> ignore
make_widget([|FStr "text"|], [|FInt 2L|], [||]) |> ignore
make_widget([||], [|FStr "text"|], [||]) |> ignore
make_widget([|FStr "text"|], [|FInt 2L|], [|FInt 3L|]) |> ignore
