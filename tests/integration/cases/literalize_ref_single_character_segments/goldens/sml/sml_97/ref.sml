datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val a_b_c : val_t = SMap [
    ("_", SStr "_")
]
val my_data : val_t = a_b_c
val _ = my_data
