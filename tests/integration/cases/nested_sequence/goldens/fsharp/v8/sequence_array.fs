module Main

type Val =
    | FNull
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val array
let my_data: Val array = [|
    FBool true;
    FStr "hi";
    FList ([|FInt 1L; FInt 2L|]);
    FNull
|]
