datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun send _ = ()
val existing : val_t = SInt 42
val _ = send(existing)
