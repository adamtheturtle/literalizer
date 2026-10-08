with A_Stub; use A_Stub;
procedure Main is
    procedure F (Value : A_Val) is begin null; end F;
begin
    F(value => AList'[AInt (1), AInt (2)]);
end Main;
