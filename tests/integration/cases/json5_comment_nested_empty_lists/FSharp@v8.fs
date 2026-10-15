module Main

type Val =
    | FList of Val list
let my_data: Val = FList [
    // outer heading
    // first empty
    FList [];
    // second empty
    FList []
]
