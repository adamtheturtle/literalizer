with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AInt (0),
        AInt (1),
        AInt (-1)
    ];
begin
    my_data := AList'[
        AInt (0),
        AInt (1),
        AInt (-1)
    ];
end Check;
