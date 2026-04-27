structure Check = struct

datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
fun process _ = ()
process("hello")
process(42)
process(SBool true)

end
