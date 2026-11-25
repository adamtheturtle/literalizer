datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val one : val_t = SInt 1
val two : val_t = SStr "s"
val my_data : val_t = SList [
    one,
    two
]
val _ = my_data
