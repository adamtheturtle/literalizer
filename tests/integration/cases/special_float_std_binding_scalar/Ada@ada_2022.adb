with A_Stub; use A_Stub;
procedure Main is
    pragma Suppress (Division_Check);
    Zero : Long_Float := 0.0;
    pragma Volatile (Zero);
    NaN : constant Long_Float := Zero / Zero;
    std : A_Val := AFloat (NaN);
begin
    null;
end Main;
