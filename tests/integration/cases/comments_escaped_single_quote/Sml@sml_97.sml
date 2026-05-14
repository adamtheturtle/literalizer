datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("key", SStr "it's here")  (* a comment *)
]
val _ = my_data
