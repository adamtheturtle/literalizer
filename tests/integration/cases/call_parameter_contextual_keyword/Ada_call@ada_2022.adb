with A_Stub; use A_Stub;
procedure Main is
    procedure F (Using : A_Val) is begin null; end F;
begin
    F(using => AInt (1));
end Main;
