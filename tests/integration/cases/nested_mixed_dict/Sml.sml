datatype val_t =
    SNull
  | SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("outer", SMap [("a", SInt 1), ("b", SStr "x"), ("c", SNull)])
]
val _ = my_data
