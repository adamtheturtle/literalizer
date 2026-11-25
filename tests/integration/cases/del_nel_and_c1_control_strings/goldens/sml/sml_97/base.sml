datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("del", SStr "a\127b"),
    ("nel", SStr "a\194\133b"),
    ("c1", SStr "a\194\159b")
]
val _ = my_data
