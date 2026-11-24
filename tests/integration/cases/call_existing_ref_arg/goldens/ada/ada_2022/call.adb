with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val) is begin null; end Process;
    existing : A_Val := AInt (42);
begin
    Process(value => existing);
end Main;
