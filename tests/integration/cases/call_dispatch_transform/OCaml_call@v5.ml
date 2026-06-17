module Check = struct

let record _ = ()
let flush _ = ()
type val_t =
  | OInt of int
  | OList of val_t list
let _ = record(42)
let _ = flush(3)

end
