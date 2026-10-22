module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "before_date" (PStr "1582-10-04")),
    (Tuple "gap_date" (PStr "1582-10-10")),
    (Tuple "transition_date" (PStr "1582-10-15")),
    (Tuple "after_date" (PStr "1582-10-16")),
    (Tuple "before_naive" (PStr "1582-10-04T12:30:00.000001")),
    (Tuple "gap_naive" (PStr "1582-10-10T12:30:00.500000")),
    (Tuple "transition_positive" (PStr "1582-10-15T00:30:00+18:00")),
    (Tuple "transition_negative" (PStr "1582-10-15T23:30:00-18:00")),
    (Tuple "after_positive" (PStr "1582-10-16T00:30:00+18:00"))
]
