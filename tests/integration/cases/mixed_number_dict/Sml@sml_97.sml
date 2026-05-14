datatype val_t =
    SInt of LargeInt.int
  | SReal of real
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SInt 1),
    ("b", SReal 2.5),
    ("c", SInt 3)
]
val _ = my_data
