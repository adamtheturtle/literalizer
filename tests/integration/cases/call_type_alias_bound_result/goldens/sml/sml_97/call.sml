fun process _ = ()
datatype val_t =
    SInt of LargeInt.int
val my_data = process(SInt 1)
val _ = my_data
