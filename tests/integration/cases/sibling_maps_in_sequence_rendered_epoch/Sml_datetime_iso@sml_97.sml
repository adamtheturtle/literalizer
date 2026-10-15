datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("k", SStr "2040-01-01T00:00:00+00:00")],
    SMap [("k", SInt 1)]
]
val _ = my_data
