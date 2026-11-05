datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("value", SList [SBool true, SBool false, SInt 0, SInt 1])
]
val _ = my_data
