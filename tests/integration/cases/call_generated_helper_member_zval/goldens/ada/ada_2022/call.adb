with A_Stub; use A_Stub;
procedure Main is
    procedure Zval (Value : A_Val) is begin null; end Zval;
begin
    Zval(value => AInt (1));
end Main;
