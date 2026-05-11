with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val; Count : A_Val) is begin null; end Process;
    my_int : A_Val := AInt (1);
    my_bool : A_Val := ABool (True);
    my_float : A_Val := AFloat (3.14);
    my_list : A_Val := AList'[
        AInt (1),
        AInt (2),
        AInt (3)
    ];
begin
    Process(value => my_int, count => AInt (42));
    Process(value => my_bool, count => AInt (7));
    Process(value => my_float, count => AInt (9));
    Process(value => my_list, count => AInt (1));
end Main;
