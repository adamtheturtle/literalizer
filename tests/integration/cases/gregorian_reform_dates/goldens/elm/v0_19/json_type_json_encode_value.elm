module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("ancient_date", Json.Encode.string "1500-03-01"),
    ("modern_date", Json.Encode.string "2024-01-15"),
    ("before_date", Json.Encode.string "1582-10-04"),
    ("gap_date", Json.Encode.string "1582-10-10"),
    ("transition_date", Json.Encode.string "1582-10-15"),
    ("after_date", Json.Encode.string "1582-10-16"),
    ("before_naive", Json.Encode.string "1582-10-04T12:30:00.000001"),
    ("gap_naive", Json.Encode.string "1582-10-10T12:30:00.500000"),
    ("transition_positive", Json.Encode.string "1582-10-15T00:30:00+18:00"),
    ("transition_negative", Json.Encode.string "1582-10-15T23:30:00-18:00"),
    ("after_positive", Json.Encode.string "1582-10-16T00:30:00+18:00")
    ]
