fun process _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = process(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26)
