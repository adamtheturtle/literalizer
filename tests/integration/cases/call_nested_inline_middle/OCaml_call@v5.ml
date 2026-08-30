module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let f _ = ()
let _ = f(OList [OList [OStr "DEL"; OStr "b"; OStr "10"]; OList [OStr "ADD"; OStr "a"; OStr "x"]])  (* note *)
(* next call *)
let _ = f(OList [OList [OStr "ADD"; OStr "c"; OStr "y"]])

end
