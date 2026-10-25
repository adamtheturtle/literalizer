module Main

let ``process`` (_value: obj) : obj = null
type HelpersType_() =
    member _.emit(__call: obj, __zip: obj) : obj = null
let helpers = HelpersType_()
type Val =
    | FInt of int64
    | FList of Val list
helpers.emit(``process``(FInt 1L), FInt 42L) |> ignore
