module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
process("hello")
process(42)
process(OBool true)

end
