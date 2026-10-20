datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun process _ = ()
val item : val_t = SList [
    SInt 1,
    SInt 2
]
val _ = process(item)
