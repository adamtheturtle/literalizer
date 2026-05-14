datatype val_t =
    SNull
  | SStr of string
  | SList of val_t list
fun process _ = ()
val _ = process(SNull)
val _ = process("hello")
