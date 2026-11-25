datatype val_t =
    SInt of LargeInt.int
  | SDatetime of ((int * int * int) * (int * int * int))
  | SList of val_t list
val my_data : val_t = SList [
    SDatetime ((2000, 1, 1), (1, 2, 3)),
    SInt 1
]
val _ = my_data
