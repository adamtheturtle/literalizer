module Check = struct

let f _ = ()
type val_t =
  | OArray of val_t array
let _ = f([||])

end
