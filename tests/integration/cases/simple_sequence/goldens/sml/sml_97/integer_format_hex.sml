datatype val_t =
    SNull
  | SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SInt 0x1,
    SStr "hello",
    SBool true,
    SNull
]
val _ = my_data
