datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun record_value _ = ()
fun flush_buffer _ = ()
fun emit _ = ()
val _ = emit(record_value(42))
val _ = flush_buffer(3)
