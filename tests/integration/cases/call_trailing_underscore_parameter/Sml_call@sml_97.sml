fun do_thing _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = do_thing(SInt 1)
val _ = do_thing(SInt 2)
