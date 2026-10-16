module Main

type Val =
    | FNull
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val array
let my_data: Val array = [|
    FInt 1L;
    FStr "hello";
    FBool true;
    FNull
|]
