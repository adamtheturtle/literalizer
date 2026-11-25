datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val shared : val_t = SList [
    SInt 1,
    SInt 2
]
val my_data : val_t = SList [
    shared,
    shared
]
val _ = my_data
