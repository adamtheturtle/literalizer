datatype val_t =
    SInt of LargeInt.int
  | SDatetime of ((int * int * int) * (int * int * int))
  | SList of val_t list
fun process _ = ()
fun emit _ = ()
val _ = emit(process(SInt 1), SDatetime ((2024, 1, 15), (12, 0, 0)))
