datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("numbers", SList [SInt 1, SInt 2]),
    ("nested", SMap [("inner", SList [SInt 3])]),
    ("mixed", SList [SInt 4, SStr "five"])
]
val _ = my_data
