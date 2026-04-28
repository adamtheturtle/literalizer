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
    process(data => my_var, count => 42);
    process(data => my_other, count => 7);
end Main;
