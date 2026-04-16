module Check

type Val =
    | FBool of bool
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FList of Val list
let mutable my_data: Val array = [|
    FInt 42L;
    FFloat 3.14;
    FBool true;
    FBool false;
    FStr "hello \"world\""
|]
