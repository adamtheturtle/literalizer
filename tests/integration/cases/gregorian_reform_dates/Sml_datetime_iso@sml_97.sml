datatype val_t =
    SStr of string
  | SDate of (int * int * int)
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("ancient_date", SDate (1500, 3, 1)),
    ("modern_date", SDate (2024, 1, 15)),
    ("before_date", SDate (1582, 10, 4)),
    ("gap_date", SDate (1582, 10, 10)),
    ("transition_date", SDate (1582, 10, 15)),
    ("after_date", SDate (1582, 10, 16)),
    ("before_naive", SStr "1582-10-04T12:30:00.000001"),
    ("gap_naive", SStr "1582-10-10T12:30:00.500000"),
    ("transition_positive", SStr "1582-10-15T00:30:00+18:00"),
    ("transition_negative", SStr "1582-10-15T23:30:00-18:00"),
    ("after_positive", SStr "1582-10-16T00:30:00+18:00")
]
val _ = my_data
