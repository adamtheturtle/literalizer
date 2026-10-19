fun first_value _ = ()
datatype val_t =
    SInt of LargeInt.int
val _ = first_value(SInt 1)
