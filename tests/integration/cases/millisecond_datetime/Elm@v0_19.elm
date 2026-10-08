module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("half", EStr "1979-05-27T07:32:00.500000"),
    ("milli", EStr "1979-05-27T07:32:00.100000"),
    ("max_milli", EStr "1979-05-27T07:32:00.999000"),
    ("whole", EStr "1979-05-27T07:32:00")
    ]
