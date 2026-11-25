fun f _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = f(SInt 1)
