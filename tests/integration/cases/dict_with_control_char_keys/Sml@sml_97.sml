datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("key\nwith\nnewlines", SStr "value1"),
    ("key\twith\ttabs", SStr "value2"),
    ("", SStr "value3")
]
val _ = my_data
