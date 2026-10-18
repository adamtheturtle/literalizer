with A_Stub; use A_Stub;
procedure Main is
    procedure Go (First_Value : A_Val; Second_Value : A_Val) is begin null; end Go;
begin
    Go(first_value => AList'[AInt (1)], second_value => AList'[AInt (2)]);
end Main;
