fun f _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = f(SList [SList [SInt 1, SInt 2], SList [SInt 3]])
