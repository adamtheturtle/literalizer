datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun process _ = ()
val repeated_var : val_t = SInt 1
val single_var : val_t = SList [
    SInt 4,
    SInt 5,
    SInt 6
]
val _ = process(repeated_var, 1)
val _ = process(single_var, 0)
val _ = process(repeated_var, 8)
