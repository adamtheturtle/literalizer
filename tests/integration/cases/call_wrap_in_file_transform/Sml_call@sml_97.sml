fun process _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val my_data = process(SInt 1, SInt 2)
val _ = my_data
