datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
  | SSet of val_t list
val my_data : val_t = SList [
    SSet [],
    SSet [SInt 1, SInt 2],
    SList []
]
val _ = my_data
