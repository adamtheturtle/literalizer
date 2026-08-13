datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_var : val_t = SInt 1
val my_data : val_t = SMap [
    ("key", my_var)
]
val _ = my_data
