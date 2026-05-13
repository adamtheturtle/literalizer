with A_Stub; use A_Stub;
procedure Main is
    procedure Process (A : A_Val; B : A_Val; C : A_Val; D : A_Val) is begin null; end Process;
begin
    Process(a => AInt (1), b => AInt (2), c => AInt (3), d => AInt (4));
    Process(a => AInt (5), b => AInt (6), c => AInt (7), d => AInt (8));
end Main;
