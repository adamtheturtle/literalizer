fun check _ = ()
datatype val_t =
    SInt of LargeInt.int
val _ = check(SInt 42)
