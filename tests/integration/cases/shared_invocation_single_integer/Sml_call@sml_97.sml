datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun consume _ = ()
val _ = consume(SInt 1)
