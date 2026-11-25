with A_Stub; use A_Stub;
procedure Main is
    procedure F (A : A_Val; B : A_Val) is begin null; end F;
begin
    F(a => AInt (2), b => AStr ("hello"));  -- trailing note
    -- next element
    F(a => AInt (3), b => AStr ("world"));
end Main;
