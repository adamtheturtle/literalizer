with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val) is begin null; end Process;
begin
    Process(value => AInt (1));  -- trail \ .
    Process(value => AInt (2));  -- second
end Main;
