datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("name", SStr "Alice"), ("age", SInt 30)],
    SMap [("name", SStr "Bob"), ("age", SInt 25)]
]
val _ = my_data
