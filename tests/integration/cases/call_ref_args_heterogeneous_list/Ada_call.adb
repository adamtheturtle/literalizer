with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Data : A_Val; Count : A_Val) is begin null; end Process;
    my_ints : A_Val := AList'[
        AInt (1),
        AInt (2),
        AInt (3)
    ];
    my_strings : A_Val := AList'[
        AStr ("a"),
        AStr ("b")
    ];
begin
    Process(data => my_ints, count => AInt (42));
    Process(data => my_strings, count => AInt (7));
end Main;
