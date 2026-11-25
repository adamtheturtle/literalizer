datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("half", SStr "1979-05-27T07:32:00.500000"),
    ("milli", SStr "1979-05-27T07:32:00.100000"),
    ("max_milli", SStr "1979-05-27T07:32:00.999000"),
    ("whole", SStr "1979-05-27T07:32:00")
]
val _ = my_data
