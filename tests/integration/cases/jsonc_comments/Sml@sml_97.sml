datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("url", SStr "https://example.org/a/*b*/"),
    ("count", SInt 2)
]
val _ = my_data
