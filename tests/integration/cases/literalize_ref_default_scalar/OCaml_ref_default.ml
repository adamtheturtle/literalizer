module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_var : val_t = OInt 1
let my_data : val_t = my_var

end
