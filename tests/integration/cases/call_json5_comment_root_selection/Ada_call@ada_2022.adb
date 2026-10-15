with A_Stub; use A_Stub;
procedure Main is
    procedure F (A : A_Val; B : A_Val) is begin null; end F;
begin
    -- selected heading
    F(a => AInt (1), b => AInt (2));  -- selected inline
end Main;
