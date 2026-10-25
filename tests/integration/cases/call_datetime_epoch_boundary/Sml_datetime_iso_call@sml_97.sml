fun consume _ = ()
datatype val_t =
    SStr of string
  | SList of val_t list
val _ = consume(SStr "1901-12-13T20:45:51")
val _ = consume(SStr "2038-01-19T03:14:08")
