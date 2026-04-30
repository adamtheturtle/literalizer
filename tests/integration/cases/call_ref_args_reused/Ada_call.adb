with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Data : A_Val; Count : A_Val) is begin null; end Process;
    shared : A_Val := AInt (1);
    other : A_Val := AInt (2);
begin
    Process(data => shared, count => AInt (1));
    Process(data => other, count => AInt (0));
    Process(data => shared, count => AInt (8));
end Main;
