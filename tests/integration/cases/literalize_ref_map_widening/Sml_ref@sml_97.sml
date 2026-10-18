datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val string_map : val_t = SMap [
    ("k", SStr "s")
]
val my_data : val_t = SList [
    string_map,
    SMap [("k", SInt 1)]
]
val _ = my_data
