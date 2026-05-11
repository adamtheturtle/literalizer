datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun process _ = ()
val _ = process(1, 2, 3, 4)
val _ = process(10, 20, 30, 40)
