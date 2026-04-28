fun process _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = process(1, 2)
val _ = process(3, 4)
