datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SInt 1),
    ("b", SStr "hello")
]
val _ = my_data
