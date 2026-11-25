with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val) is begin null; end Process;
    value : A_Val := AInt (1);
begin
    Process(value => value);
end Main;
