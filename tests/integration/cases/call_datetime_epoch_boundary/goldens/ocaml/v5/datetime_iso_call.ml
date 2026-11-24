module Check = struct

let consume _ = ()
type val_t =
  | OStr of string
  | OList of val_t list
let _ = consume(OStr "1901-12-13T20:45:51")
let _ = consume(OStr "2038-01-19T03:14:08")

end
