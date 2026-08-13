datatype val_t =
    SStr of string
  | SInt of LargeInt.int
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("ts", SInt 32535215999)
]
val _ = my_data
