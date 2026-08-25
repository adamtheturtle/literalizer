module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OList [OInt 2; OStr "hello"];  (* trailing note *)
    (* next element *)
    OList [OInt 3; OStr "world"]
]

end
