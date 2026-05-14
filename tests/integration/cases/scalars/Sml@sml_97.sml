datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SReal of real
  | SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SInt 42,
    SReal 3.14,
    SBool true,
    SBool false,
    SStr "hello \"world\""
]
val _ = my_data
