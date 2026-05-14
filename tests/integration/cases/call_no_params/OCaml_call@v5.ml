module Check = struct

type val_t =
  | OList of val_t list
let process _ = ()
let _ = process()
let _ = process()

end
