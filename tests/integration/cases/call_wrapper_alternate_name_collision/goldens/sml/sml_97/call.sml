fun check_wrapper _ = ()
datatype val_t =
    SInt of LargeInt.int
val _ = check_wrapper(SInt 42)
