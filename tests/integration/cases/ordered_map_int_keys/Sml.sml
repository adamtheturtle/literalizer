datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("1", SStr "one"),
    ("2", SStr "two"),
    ("42", SStr "answer")
]
val _ = my_data
