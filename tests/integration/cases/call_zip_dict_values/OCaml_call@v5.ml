module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let process _ = ()
let emit _ = ()
let _ = emit(process("hello"), OMap [("a", OInt 1); ("b", OInt 2)])
let _ = emit(process(42), OMap [("c", OInt 3); ("d", OInt 4)])

end
