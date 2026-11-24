module Check = struct

type val_t =
  | ONull
  | OList of val_t list
let consume _ = ()
let my_null : val_t = ONull
let regular_null : val_t = ONull
let _ = consume(my_null)
let _ = consume(regular_null)

end
