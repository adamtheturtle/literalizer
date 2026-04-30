module Check = struct

type val_t =
  | OList of val_t list
let process _ = ()
let emit _ = ()
let _ = emit(process())
let _ = emit(process())

end
