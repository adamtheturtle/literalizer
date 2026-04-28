with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Data : A_Val) is begin null; end Process;
    my_var : A_Val := AList'[
        AInt (1),
        AInt (2),
        AInt (3)
    ];
begin
    process(data => my_var);
end Main;
