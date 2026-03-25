module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    (* line 1 *)
    (* line 2 *)
    OStr "a"
]

end
