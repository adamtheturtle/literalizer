datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun process _ = ()
val _ = process(~1)
val _ = process(~2)
val _ = process(~3)
