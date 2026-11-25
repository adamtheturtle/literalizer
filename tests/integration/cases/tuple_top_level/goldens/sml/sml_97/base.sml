datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SInt 1,
    SStr "email",
    SStr "a@gmail.com",
    SInt 100
]
val _ = my_data
