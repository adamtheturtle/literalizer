fun record_entry _ = ()
datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val my_data = record_entry(SStr "a", SInt 1, SBool true)
val _ = my_data
