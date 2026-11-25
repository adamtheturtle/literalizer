fun process _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = process(SInt 0, SInt 1, SInt 2, SInt 3, SInt 4, SInt 5, SInt 6, SInt 7, SInt 8, SInt 9, SInt 10, SInt 11, SInt 12, SInt 13, SInt 14, SInt 15, SInt 16, SInt 17, SInt 18, SInt 19, SInt 20, SInt 21, SInt 22, SInt 23, SInt 24, SInt 25, SInt 26)
