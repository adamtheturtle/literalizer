datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    (* server *)
    ("host", SStr "localhost")  (* default *)
]
val _ = my_data
