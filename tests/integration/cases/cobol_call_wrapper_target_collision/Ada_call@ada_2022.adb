with A_Stub; use A_Stub;
procedure Main is
    procedure Check (A : A_Val) is begin null; end Check;
begin
    Check(a => AInt (42));
end Main;
