module Check = struct

type val_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t array = [|
    OMap [("a", OInt 1)];
    OInt 1;
    OStr "x";
    OBool true;
    OFloat 2.5;
    ONull
|]

end
