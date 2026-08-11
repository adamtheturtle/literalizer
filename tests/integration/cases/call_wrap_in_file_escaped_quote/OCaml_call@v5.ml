module Check = struct

let process _ = ()
type val_t =
  | OStr of string
  | OList of val_t list
let _ = process(OStr "a\"b")

end
