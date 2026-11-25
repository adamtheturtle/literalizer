with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Xs : A_Val) is begin null; end Process;
begin
    Process(xs => AList'[
        AInt (1),
        AInt (2)
    ]);
    Process(xs => AList'[
        AInt (3)
    ]);
end Main;
