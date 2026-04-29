datatype val_t =
    SStr of string
  | SList of val_t list
fun process _ = ()
(* Test cases *)
val _ = process("hello")  (* single word *)
val _ = process("hello world")  (* two words *)
(* trailing comment *)
