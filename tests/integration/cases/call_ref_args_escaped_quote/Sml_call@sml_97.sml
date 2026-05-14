datatype val_t =
    SStr of string
  | SList of val_t list
fun process _ = ()
val my_str : val_t = SStr "a\"b"
val _ = process(my_str)
