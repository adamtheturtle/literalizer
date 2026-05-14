datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("id", SInt 1), ("label", SStr "first")],
    SMap [("id", SInt 2), ("label", SStr "second")],
    SMap [("id", SInt 3), ("label", SStr "third")]
]
val _ = my_data
