datatype val_t =
    SReal of real
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("value", SReal (~0.0))
]
val _ = my_data
