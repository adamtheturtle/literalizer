module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let process _ = ()
(* Test cases *)
let _ = process(OStr "hello")  (* single word *)
let _ = process(OStr "hello world")  (* two words *)
(* trailing comment *)

end
