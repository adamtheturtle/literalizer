datatype val_t =
    SNull
  | SInt of LargeInt.int
  | SList of val_t list
fun consume _ = ()
val item : val_t = SNull
val _ = consume(item)
