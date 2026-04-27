structure Check = struct

datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun process _ = ()
process(1, 42)
process(2, 100)

end
