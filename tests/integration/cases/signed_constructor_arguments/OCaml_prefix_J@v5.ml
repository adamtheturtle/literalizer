module Check = struct

type val_t =
  | JInt of int
  | JFloat of float
  | JList of val_t list
let my_data : val_t = JList [
    JInt (-42);
    JInt 0;
    JInt 42;
    JFloat (-1.25);
    JFloat 0.0;
    JFloat 1.25
]

end
