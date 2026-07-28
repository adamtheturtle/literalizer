datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun process _ = ()
val unknown_value : val_t = SList [
    SInt 1
]
val _ = process(unknown_value)
