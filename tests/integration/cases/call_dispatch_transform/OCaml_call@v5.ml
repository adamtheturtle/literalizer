module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let record_value _ = ()
let flush_buffer _ = ()
let emit _ = ()
let _ = emit(record_value(42))
let _ = flush_buffer(3)

end
