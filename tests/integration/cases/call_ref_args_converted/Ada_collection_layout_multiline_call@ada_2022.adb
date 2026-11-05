with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Data : A_Val; Count : A_Val) is begin null; end Process;
    my_var : A_Val := AList'[
        AInt (1),
        AInt (2),
        AInt (3)
    ];
    my_other : A_Val := AList'[
        AInt (4),
        AInt (5),
        AInt (6)
    ];
begin
    Process(data => my_var, count => AInt (42));
    Process(data => my_other, count => AInt (7));
end Main;
