module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
    | FDate of System.DateOnly
let my_data: Val = FMap [
    ("ancient_date", FDate (System.DateOnly(1500, 3, 1)));
    ("modern_date", FDate (System.DateOnly(2024, 1, 15)));
    ("before_date", FDate (System.DateOnly(1582, 10, 4)));
    ("gap_date", FDate (System.DateOnly(1582, 10, 10)));
    ("transition_date", FDate (System.DateOnly(1582, 10, 15)));
    ("after_date", FDate (System.DateOnly(1582, 10, 16)));
    ("before_naive", FStr "1582-10-04T12:30:00.000001");
    ("gap_naive", FStr "1582-10-10T12:30:00.500000");
    ("transition_positive", FStr "1582-10-15T00:30:00+18:00");
    ("transition_negative", FStr "1582-10-15T23:30:00-18:00");
    ("after_positive", FStr "1582-10-16T00:30:00+18:00")
]
