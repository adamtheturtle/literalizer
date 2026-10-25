with A_Stub; use A_Stub;
procedure Main is
    pragma Suppress (Division_Check);
    Zero : Long_Float := 0.0;
    pragma Volatile (Zero);
    NaN : constant Long_Float := Zero / Zero;
    Neg_Inf : constant Long_Float := -1.0 / Zero;
    Pos_Inf : constant Long_Float := 1.0 / Zero;
    procedure Capture (Nan_Value : A_Val; Positive_Infinity : A_Val; Negative_Infinity : A_Val; Finite_Value : A_Val; Date_Value : A_Val; Datetime_Value : A_Val; Text_Value : A_Val) is begin null; end Capture;
begin
    Capture(nan_value => AFloat (NaN), positive_infinity => AFloat (Pos_Inf), negative_infinity => AFloat (Neg_Inf), finite_value => AFloat (1.25), date_value => AStr ("2024-01-15"), datetime_value => AStr ("2024-01-15T12:34:56"), text_value => AStr ("[ordinary text]"));
end Main;
