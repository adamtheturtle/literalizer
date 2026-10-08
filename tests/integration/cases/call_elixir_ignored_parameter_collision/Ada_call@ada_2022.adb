with A_Stub; use A_Stub;
procedure Main is
    procedure F (X : A_Val; X : A_Val) is begin null; end F;
begin
    F(x => AInt (1), _x => AInt (2));
end Main;
