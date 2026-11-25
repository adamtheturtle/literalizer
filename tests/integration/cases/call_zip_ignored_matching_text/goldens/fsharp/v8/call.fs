module Main

type Val =
    | FStr of string
    | FList of Val list
let ``process`` (_value: obj) : obj = null
``process``(FStr "time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC)") |> ignore
