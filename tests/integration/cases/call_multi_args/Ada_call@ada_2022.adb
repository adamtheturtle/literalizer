with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val; Count : A_Val) is begin null; end Process;
begin
    Process(value => AInt (1), count => AInt (42));
    Process(value => AInt (2), count => AInt (100));
end Main;
