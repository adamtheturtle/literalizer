module Check

type Val =
    | FSet of Val list
let mutable my_data: Val = FSet []
