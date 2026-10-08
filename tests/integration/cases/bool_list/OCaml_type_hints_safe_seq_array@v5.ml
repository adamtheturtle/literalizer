module Check = struct

type val_t =
  | OBool of bool
  | OArray of val_t array
let my_data : val_t array = [|
    OBool true;
    OBool false;
    OBool true
|]

end
