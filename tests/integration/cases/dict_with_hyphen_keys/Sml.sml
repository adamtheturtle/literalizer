datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("my-key", SStr "value1"),
    ("another-key", SStr "value2"),
    ("normal_key", SStr "value3")
]
val _ = my_data
