fun record _ = ()
fun flush _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = record(42)
val _ = flush(3)
