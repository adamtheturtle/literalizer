datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("exact_millisecond", SStr "09:30:15.123000"),
    ("sub_millisecond", SStr "09:30:15.123456")
]
val _ = my_data
