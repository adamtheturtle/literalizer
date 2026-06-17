fun store_item _ = ()
fun read_item _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = store_item(1, 10)
val _ = read_item(1)
