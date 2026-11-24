datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("plain", SList [SInt 1, SInt 2]),
    ("with-dash", SStr "a\nb")
]
val _ = my_data
