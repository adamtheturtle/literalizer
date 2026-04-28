with A_Stub; use A_Stub;
procedure Main is
    procedure Process (A : A_Val; B : A_Val) is begin null; end Process;
begin
    process(a => 1, b => 2);
    process(a => 3, b => 4);
end Main;
