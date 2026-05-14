with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val) is begin null; end Process;
begin
    Process(value => AStr ("hello"));
    Process(value => AInt (42));
    Process(value => ABool (True));
end Main;
