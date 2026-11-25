datatype val_t =
    SNull
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("nil", SList [SList [SList [SList [SList [SList [SList [SList [SList [SNull]]]]]]]]]),
    ("empty", SList [SList [SList [SList [SList [SList [SList [SList [SList [SList []]]]]]]]]]),
    ("siblings", SList [SList [SList [SList [SList [SList [SList [SList [SList [SList [SInt 4, SInt 5]]]]]]]]]])
]
val _ = my_data
