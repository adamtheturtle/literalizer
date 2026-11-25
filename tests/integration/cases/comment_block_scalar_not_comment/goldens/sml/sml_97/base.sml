datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("description", SStr "# not a comment\n"),
    ("name", SStr "foo")
]
val _ = my_data
