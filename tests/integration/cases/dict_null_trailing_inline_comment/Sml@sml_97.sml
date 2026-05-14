datatype val_t =
    SNull
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("host", SStr "localhost"),
    ("port", SNull)  (* not configured yet *)
]
val _ = my_data
