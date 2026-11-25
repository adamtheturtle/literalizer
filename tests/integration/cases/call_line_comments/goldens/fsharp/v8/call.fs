module Main

type Val =
    | FStr of string
    | FList of Val list
let ``process`` (_value: obj) : obj = null
``process``(FStr "Dune") |> ignore  // first edition
``process``(FStr "Solaris") |> ignore
``process``(FStr "Neuromancer") |> ignore  // cyberpunk
