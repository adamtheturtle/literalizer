module Main

type Val =
    | FNull
    | FBool of bool
    | FFloat of float
    | FList of Val list
    | FDate of System.DateOnly
    | FDatetime of System.DateTime
let my_data: Val = FList [
    FBool true;
    FFloat 1.5;
    FNull;
    FDate (System.DateOnly(2020, 1, 1));
    FDatetime (System.DateTime(2020, 1, 1, 0, 0, 0));
    FList []
]
