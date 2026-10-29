module Check = struct

type val_t =
  | ONull
  | OInt of int
  | OArray of val_t array
let process _ = ()
let _ = process(ONull)
let _ = process([|OInt 1; OInt 2|])

end
