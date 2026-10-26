module Check = struct

type val_t =
  | ONull
  | OList of val_t list
let value : val_t = ONull
let my_data : val_t = OList [
    value;
    value;
    ONull
]

end
