module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("half", FStr "1979-05-27T07:32:00.500000");
    ("milli", FStr "1979-05-27T07:32:00.100000");
    ("max_milli", FStr "1979-05-27T07:32:00.999000");
    ("whole", FStr "1979-05-27T07:32:00")
]
