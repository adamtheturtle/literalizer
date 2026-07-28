datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun process _ = ()
val known_value : val_t = SInt 1
val unknown_value : val_t = SList []
val _ = process(unknown_value)
