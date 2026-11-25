with A_Stub; use A_Stub;
procedure Main is
    pragma Suppress (Division_Check);
    Zero : Long_Float := 0.0;
    pragma Volatile (Zero);
    NaN : constant Long_Float := Zero / Zero;
    Neg_Inf : constant Long_Float := -1.0 / Zero;
    Pos_Inf : constant Long_Float := 1.0 / Zero;
    std : A_Val := AMap'[
        AEntry ("nan", AFloat (NaN)),
        AEntry ("positive", AFloat (Pos_Inf)),
        AEntry ("negative", AFloat (Neg_Inf))
    ];
begin
    null;
end Main;
