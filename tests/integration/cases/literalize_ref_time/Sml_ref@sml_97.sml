datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_time : val_t = SStr "01:02:03"
val my_data : val_t = SMap [
    ("x", my_time)
]
val _ = my_data
