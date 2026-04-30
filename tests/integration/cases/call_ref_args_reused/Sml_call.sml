datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun process _ = ()
val shared : val_t = SInt 1
val other : val_t = SInt 2
val _ = process(shared, 1)
val _ = process(other, 0)
val _ = process(shared, 8)
