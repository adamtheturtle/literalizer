module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let process _ = ()
let existing : val_t = OInt 42
let _ = process(existing)

end
