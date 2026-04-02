module Check

type Val =
    | FList of Val list
let mutable my_data: Val = FList [
    FList [];
    FList []
]
