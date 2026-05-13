module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_int : val_t = OInt 42
let my_data : val_t = my_int

end
