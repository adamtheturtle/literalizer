datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val shared : val_t = SList [
    SInt 1,
    SStr "x"
]
val my_data : val_t = SList [
    shared,
    shared
]
val _ = my_data
