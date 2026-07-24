datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("id", SInt 100), ("label", SStr "first item"), ("enabled", SBool false), ("related_ids", SList [SInt 102, SInt 103])],
    SMap [("id", SInt 101), ("label", SStr "second item"), ("enabled", SBool true), ("related_ids", SList [SInt 100])]
]
val _ = my_data
