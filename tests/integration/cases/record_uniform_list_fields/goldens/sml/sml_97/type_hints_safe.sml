datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("scores", SList [SInt 1, SInt 2])],
    SMap [("scores", SList [SInt 3, SInt 4])]
]
val _ = my_data
