datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    (* event time *)
    ("when", SStr "2024-01-15T12:34:56+00:00")
]
val _ = my_data
