datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun consume _ = ()
val external_value : val_t = SInt 1
val _ = consume(external_value)
