with A_Stub; use A_Stub;
procedure Main is
    procedure F (A : A_Val) is begin null; end F;
begin
    F(a => AList'[AInt (1)]);  -- note
end Main;
