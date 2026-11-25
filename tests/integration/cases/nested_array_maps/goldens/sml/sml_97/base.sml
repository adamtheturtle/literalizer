datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("groups", SList [SList [SMap [("id", SInt 1)]], SList [SMap [("id", SInt 2)]]])
]
val _ = my_data
