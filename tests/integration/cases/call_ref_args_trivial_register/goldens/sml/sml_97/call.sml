datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SReal of real
  | SList of val_t list
fun process _ = ()
val my_int : val_t = SInt 1
val my_bool : val_t = SBool true
val my_float : val_t = SReal 3.14
val my_list : val_t = SList [
    SInt 1,
    SInt 2,
    SInt 3
]
val _ = process(my_int, SInt 42)
val _ = process(my_bool, SInt 7)
val _ = process(my_float, SInt 9)
val _ = process(my_list, SInt 1)
