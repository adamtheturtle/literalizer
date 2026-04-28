with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val; Count : A_Val) is begin null; end Process;
begin
    process(value => 1, count => 42);
    process(value => 2, count => 100);
end Main;
