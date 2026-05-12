module Check = struct

type val_t =
  | ONull
  | OStr of string
  | OList of val_t list
let process _ = ()
let _ = process(ONull)
let _ = process("hello")

end
