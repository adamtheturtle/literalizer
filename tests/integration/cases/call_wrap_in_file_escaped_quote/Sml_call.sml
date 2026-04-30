fun process _ = ()
datatype val_t =
    SStr of string
  | SList of val_t list
val _ = process("a\"b")
