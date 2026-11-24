with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val) is begin null; end Process;
begin
    Process(value => AStr ("09:30:00"));
    Process(value => AStr ("2024-01-15T00:00:00+00:00"));
    Process(value => AInt (1));
end Main;
