module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let consume _ = ()
let item : val_t = OStr "s"
let _ = consume(item)

end
