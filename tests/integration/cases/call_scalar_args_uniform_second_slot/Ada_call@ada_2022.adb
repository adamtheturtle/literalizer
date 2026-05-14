with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val; Label : A_Val) is begin null; end Process;
begin
    Process(value => AStr ("hello"), label => AStr ("a"));
    Process(value => AInt (42), label => AStr ("b"));
    Process(value => ABool (True), label => AStr ("c"));
end Main;
