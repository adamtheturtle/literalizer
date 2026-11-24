datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("key", SStr "value \" # not a comment")  (* real *)
]
val _ = my_data
