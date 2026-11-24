with A_Stub; use A_Stub;
procedure Main is
    procedure F (A : A_Val) is begin null; end F;
begin
    -- scalar heading
    -- second heading line
    -- scalar inline
    -- inline continuation
    -- scalar trailing
    F(a => AInt (42));
end Main;
