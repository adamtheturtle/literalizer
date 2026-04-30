module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let process _ = ()
let my_str : val_t = OStr "a\"b"
let _ = process(my_str)

end
