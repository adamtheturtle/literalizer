module Check = struct

type val_t =
  | ONull
  | OBool of bool
  | OFloat of float
  | ODate of (int * int * int)
  | ODatetime of ((int * int * int) * (int * int * int))
  | OList of val_t list
let my_data : val_t = OList [
    OBool true;
    OFloat 1.5;
    ONull;
    ODate (2020, 1, 1);
    ODatetime ((2020, 1, 1), (0, 0, 0));
    OList []
]

end
