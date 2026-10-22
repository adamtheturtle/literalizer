datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("single_map", SList [SMap []]),
    ("single_list", SList [SList [SInt 1]]),
    ("single_deep", SList [SList [SList [SInt 2]]])
]
val _ = my_data
