module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
let process _ = ()
let emit _ = ()
let _ = emit(process("hello"), 1)
let _ = emit(process(42), 0)

end
