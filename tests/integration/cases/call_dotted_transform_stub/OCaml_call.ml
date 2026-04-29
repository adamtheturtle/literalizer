module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
let process _ = ()
module Tracer = struct
let emit _ = ()
end
let _ = tracer.emit(process("hello"))
let _ = tracer.emit(process(42))
let _ = tracer.emit(process(OBool true))

end
