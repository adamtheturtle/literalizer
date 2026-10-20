datatype val_t =
    SNull
  | SList of val_t list
fun consume _ = ()
val my_null : val_t = SNull
val regular_null : val_t = SNull
val _ = consume(my_null)
val _ = consume(regular_null)
