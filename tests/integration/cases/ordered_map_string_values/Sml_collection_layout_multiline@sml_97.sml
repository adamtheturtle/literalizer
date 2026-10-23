datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("first", SStr "one"),
    ("second", SStr "two"),
    ("third", SStr "three")
]
val _ = my_data
