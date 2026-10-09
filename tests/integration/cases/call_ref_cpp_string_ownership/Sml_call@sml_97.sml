datatype val_t =
    SStr of string
  | SList of val_t list
fun consume _ = ()
val item : val_t = SStr "s"
val _ = consume(item)
