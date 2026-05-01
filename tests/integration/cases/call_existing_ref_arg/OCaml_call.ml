module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let send _ = ()
let existing : val_t = OInt 42
let _ = send(existing)

end
