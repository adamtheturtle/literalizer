with A_Stub; use A_Stub;
procedure Main is
    procedure F (A : A_Val) is begin null; end F;
begin
    F(a => AList'[AList'[AInt (1), AInt (2)], AList'[AInt (3)]]);
end Main;
