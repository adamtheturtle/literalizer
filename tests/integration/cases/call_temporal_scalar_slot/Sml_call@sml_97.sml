datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SDatetime of ((int * int * int) * (int * int * int))
  | SList of val_t list
fun process _ = ()
val _ = process(SStr "09:30:00")
val _ = process(SDatetime ((2024, 1, 15), (0, 0, 0)))
val _ = process(SInt 1)
