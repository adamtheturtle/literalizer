fun consume _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = consume(SInt (~2147483649))
val _ = consume(SInt 2147483648)
