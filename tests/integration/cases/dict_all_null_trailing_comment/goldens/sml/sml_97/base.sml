datatype val_t =
    SNull
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SNull),
    ("b", SNull)
    (* trailing *)
]
val _ = my_data
