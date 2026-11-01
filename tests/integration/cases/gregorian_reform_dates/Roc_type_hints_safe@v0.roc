module [my_data]

Val : [
    RStr Str,
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("ancient_date", RStr "1500-03-01"),
    ("modern_date", RStr "2024-01-15"),
    ("before_date", RStr "1582-10-04"),
    ("gap_date", RStr "1582-10-10"),
    ("transition_date", RStr "1582-10-15"),
    ("after_date", RStr "1582-10-16"),
    ("before_naive", RStr "1582-10-04T12:30:00.000001"),
    ("gap_naive", RStr "1582-10-10T12:30:00.500000"),
    ("transition_positive", RStr "1582-10-15T00:30:00+18:00"),
    ("transition_negative", RStr "1582-10-15T23:30:00-18:00"),
    ("after_positive", RStr "1582-10-16T00:30:00+18:00"),
]
