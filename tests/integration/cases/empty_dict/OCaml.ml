module Check = struct

type val_t =
  | OMap of (string * val_t) list
let my_data : val_t = OMap []

end
