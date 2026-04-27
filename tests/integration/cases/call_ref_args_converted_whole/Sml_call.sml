structure Check = struct

datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun process _ = ()
val my_var : val_t = SList [
    SInt 1,
    SInt 2,
    SInt 3
]
val _ = process(my_var)

end
