module Main

let consume (_value: obj) : obj = null
type Val =
    | FList of Val list
    | FStr of string
consume(FStr "1901-12-13T20:45:51") |> ignore
consume(FStr "2038-01-19T03:14:08") |> ignore
