module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("stamps", EList [EStr "2001-02-03T04:05:06+00:00:01", EStr "2001-02-03T04:05:06-00:00:01", EStr "2001-02-03T04:05:06+00:00:00.000001", EStr "2001-02-03T04:05:06-00:00:00.000001", EStr "2001-02-03T04:05:06+05:30:15.000001", EStr "2001-02-03T04:05:06-05:30:15.000001"])
    ]
