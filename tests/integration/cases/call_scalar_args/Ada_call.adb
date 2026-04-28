with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val) is begin null; end Process;
begin
    process(value => "hello");
    process(value => 42);
    process(value => ABool (True));
end Main;
