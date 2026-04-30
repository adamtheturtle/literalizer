with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Data : A_Val; Count : A_Val) is begin null; end Process;
    single_var : A_Val := AList'[
        AInt (4),
        AInt (5),
        AInt (6)
    ];
    repeated_var : A_Val := AInt (1);
begin
    Process(data => repeated_var, count => AInt (1));
    Process(data => single_var, count => AInt (0));
    Process(data => repeated_var, count => AInt (8));
end Main;
