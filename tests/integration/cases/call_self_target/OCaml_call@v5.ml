module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let self _ = ()
let _ = self(OStr "hello")

end
