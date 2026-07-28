datatype val_t =
    SBool of bool
  | SList of val_t list
fun process _ = ()
val known_value : val_t = SBool true
val unknown_value : val_t = SBool true
val _ = process(known_value, SList [unknown_value])
