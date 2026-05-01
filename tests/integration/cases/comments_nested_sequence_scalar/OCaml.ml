module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OList [OStr "ADD"; OStr "alice"; OStr "hello"];
    OList [OStr "DEL"; OStr "bob"; OStr "5"]  (* removes "world" *)
]

end
