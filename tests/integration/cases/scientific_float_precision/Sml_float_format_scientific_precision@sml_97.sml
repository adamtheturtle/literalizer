datatype val_t =
    SReal of real
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("pi", SReal 3.141592653589793)
]
val _ = my_data
