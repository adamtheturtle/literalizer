module Main

let make_widget (_before: obj, _populated: obj, _after: obj) : obj = null
type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
make_widget(FList [], FList [FInt 1L], FList []) |> ignore
make_widget(FList [FStr "text"], FList [FInt 2L], FList []) |> ignore
make_widget(FList [], FList [FStr "text"], FList []) |> ignore
make_widget(FList [FStr "text"], FList [FInt 2L], FList [FInt 3L]) |> ignore
