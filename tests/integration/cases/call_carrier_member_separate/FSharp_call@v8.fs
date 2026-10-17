module Main

type AppType_() =
    member _.go(_first_value: obj, _second_value: obj) : obj = null
let app = AppType_()
type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
app.go(FList [FInt 1L], FList [FStr "text"]) |> ignore
