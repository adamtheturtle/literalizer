datatype val_t =
    SInt of LargeInt.int
val my_data : val_t = SInt (* scalar heading *)
(* second heading line *)
0x2a  (* scalar inline *)
(* inline continuation *)
(* scalar trailing *)
val _ = my_data
