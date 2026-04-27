structure Check = struct

fun process _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
process(1, 2)
process(3, 4)

end
