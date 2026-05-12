datatype val_t =
    SNull
  | SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SBool true,
    SStr "hi",
    SList [SInt 1, SInt 2],
    SNull
]
val _ = my_data
