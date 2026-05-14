module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let op _ = ()
let _ = op("hello")

end
