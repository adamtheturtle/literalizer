datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val sibling_map : val_t = SMap [
    ("k", SInt 2)
]
val my_data : val_t = SList [
    SMap [("k", SInt 1)],
    sibling_map
]
val _ = my_data
