module Main

type Val =
    | FBool of bool
let refFlag: Val = FBool true
let my_data: Val = refFlag
