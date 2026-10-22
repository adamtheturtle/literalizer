datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("first", SList [SList [SInt 1, SStr "value"], SList []]),
    ("second", SList [SList [], SList [SInt 2, SStr "other"]])
]
val _ = my_data
