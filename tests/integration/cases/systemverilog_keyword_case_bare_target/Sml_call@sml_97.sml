fun Before _ = ()
datatype val_t =
    SInt of LargeInt.int
val _ = Before(SInt 1)
