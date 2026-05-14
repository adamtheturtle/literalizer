with A_Stub; use A_Stub;
procedure Main is
    procedure Process (A : A_Val; B : A_Val) is begin null; end Process;
begin
    Process(a => AInt (1), b => AInt (2));
    Process(a => AInt (3), b => AInt (4));
end Main;
