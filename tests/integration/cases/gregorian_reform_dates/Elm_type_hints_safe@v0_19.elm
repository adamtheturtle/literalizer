module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("ancient_date", EStr "1500-03-01"),
    ("modern_date", EStr "2024-01-15"),
    ("before_date", EStr "1582-10-04"),
    ("gap_date", EStr "1582-10-10"),
    ("transition_date", EStr "1582-10-15"),
    ("after_date", EStr "1582-10-16"),
    ("before_naive", EStr "1582-10-04T12:30:00.000001"),
    ("gap_naive", EStr "1582-10-10T12:30:00.500000"),
    ("transition_positive", EStr "1582-10-15T00:30:00+18:00"),
    ("transition_negative", EStr "1582-10-15T23:30:00-18:00"),
    ("after_positive", EStr "1582-10-16T00:30:00+18:00")
    ]
