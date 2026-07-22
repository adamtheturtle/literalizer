datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("missing", SInt (~1)), ("present", SInt 1)],
    SMap [("missing", SInt 2), ("present", SInt 3)]
]
val _ = my_data
