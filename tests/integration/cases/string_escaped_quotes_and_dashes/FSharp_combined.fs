module Check

type Val =
    | FStr of string
let mutable my_data: Val = FStr "hello \"world\" -- not a comment"
