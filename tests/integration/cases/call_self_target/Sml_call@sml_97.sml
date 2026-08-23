datatype val_t =
    SStr of string
  | SList of val_t list
fun self _ = ()
val _ = self(SStr "hello")
