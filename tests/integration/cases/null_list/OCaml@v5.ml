module Check = struct

type val_t =
  | ONull
  | OList of val_t list
let my_data : val_t = OList [
    ONull;
    ONull
]

end
