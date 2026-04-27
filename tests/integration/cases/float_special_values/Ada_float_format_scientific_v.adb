with A_Stub; use A_Stub;
procedure Check is
    pragma Suppress (Division_Check);
    Zero : Long_Float := 0.0;
    pragma Volatile (Zero);
    NaN : constant Long_Float := Zero / Zero;
    Neg_Inf : constant Long_Float := -1.0 / Zero;
    Pos_Inf : constant Long_Float := 1.0 / Zero;
    my_data : A_Val := AList'[
        AFloat (Pos_Inf),
        AFloat (Neg_Inf),
        AFloat (NaN)
    ];
begin
    null;
end Check;
