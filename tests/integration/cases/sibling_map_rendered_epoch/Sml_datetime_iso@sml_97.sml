datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SMap [("k", SStr "2040-01-01T00:00:00+00:00")]),
    ("b", SMap [("k", SInt 1)])
]
val _ = my_data
