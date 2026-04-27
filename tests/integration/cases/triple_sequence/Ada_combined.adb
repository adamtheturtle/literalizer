with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AInt (1),
        AStr ("hello"),
        ABool (True)
    ];
begin
    my_data := AList'[
        AInt (1),
        AStr ("hello"),
        ABool (True)
    ];
end Check;
