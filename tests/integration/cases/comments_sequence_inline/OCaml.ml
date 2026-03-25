module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OStr "a";  (* note a *)
    OStr "b"  (* note b *)
]

end
