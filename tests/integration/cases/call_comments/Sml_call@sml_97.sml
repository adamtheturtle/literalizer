datatype val_t =
    SStr of string
  | SList of val_t list
fun process _ = ()
(* Test cases *)
val _ = process(SStr "hello")  (* single word *)
val _ = process(SStr "hello world")  (* two words *)
(* trailing comment *)
