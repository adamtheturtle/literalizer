module Main

type Val =
    | FNull
    | FBool of bool
    | FFloat of float
    | FList of Val list
    | FStr of string
    | FDate of System.DateTime
    | FDatetime of System.DateTime
let my_data: Val = FList [
    FBool true;
    FFloat 1.5;
    FNull;
    FStr (string (System.DateOnly(2020, 1, 1)));
    FStr (string (System.DateTime(2020, 1, 1, 0, 0, 0)));
    FList []
]
