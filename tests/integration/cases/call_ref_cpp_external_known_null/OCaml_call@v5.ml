module Check = struct

type val_t =
  | ONull
let consume _ = ()
let item : val_t = ONull
let _ = consume(item)

end
