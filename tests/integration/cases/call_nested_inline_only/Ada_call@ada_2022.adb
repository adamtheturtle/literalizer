with A_Stub; use A_Stub;
procedure Main is
    procedure F (A : A_Val; B : A_Val) is begin null; end F;
begin
    F(a => AInt (2), b => AStr ("hello"));  -- trailing note
    F(a => AInt (3), b => AStr ("world"));  -- another note
end Main;
