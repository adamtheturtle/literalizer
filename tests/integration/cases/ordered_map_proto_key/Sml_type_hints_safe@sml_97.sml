datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("__proto__", SMap [("x", SInt 1)]),
    ("ordinary", SInt 2)
]
val _ = my_data
