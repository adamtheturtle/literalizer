datatype val_t =
    SStr of string
  | SList of val_t list
fun process _ = ()
val _ = process(SStr "time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC)")
