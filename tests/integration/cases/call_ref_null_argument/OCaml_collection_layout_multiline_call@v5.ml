module Check = struct

type val_t =
  | ONull
let consume _ = ()
let value : val_t = ONull
let _ = consume(value)

end
