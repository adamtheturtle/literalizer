module Check

type Val =
    | FSet of Val list
let my_data: Val = FSet []
