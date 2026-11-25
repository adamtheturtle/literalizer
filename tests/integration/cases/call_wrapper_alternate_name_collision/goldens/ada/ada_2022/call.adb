with A_Stub; use A_Stub;
procedure Main is
    procedure Check_Wrapper (A : A_Val) is begin null; end Check_Wrapper;
begin
    Check_Wrapper(a => AInt (42));
end Main;
