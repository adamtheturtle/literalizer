datatype val_t =
    SNull
  | SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SList [],
    SList [SInt 1],
    SList [SInt 1, SInt 2],
    SList [SInt 1, SStr "x", SBool true, SNull],
    SList [SInt 1, SInt 2, SInt 3, SInt 4, SInt 5, SInt 6, SInt 7, SInt 8]
]
val _ = my_data
