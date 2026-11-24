with A_Stub; use A_Stub;
procedure Main is
    procedure F (A : A_Val; B : A_Val) is begin null; end F;
begin
    -- calls heading
    -- before call one
    -- first argument
    F(a => AInt (1), b => AInt (2));  -- after call one
    -- second argument
    F(a => AInt (3), b => AInt (4));
    -- after all calls
end Main;
