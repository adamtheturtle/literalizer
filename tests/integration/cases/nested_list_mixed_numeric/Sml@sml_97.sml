datatype val_t =
    SInt of LargeInt.int
  | SReal of real
  | SList of val_t list
val my_data : val_t = SList [
    SList [SInt 1],
    SList [SReal 2.5]
]
val _ = my_data
