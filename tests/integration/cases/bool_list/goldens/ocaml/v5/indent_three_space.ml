module Check = struct

type val_t =
  | OBool of bool
  | OList of val_t list
let my_data : val_t = OList [
   OBool true;
   OBool false;
   OBool true
]

end
