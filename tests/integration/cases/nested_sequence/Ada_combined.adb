with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        ABool (True),
        AStr ("hi"),
        AList'[AInt (1), AInt (2)],
        ANull
    ];
begin
    my_data := AList'[
        ABool (True),
        AStr ("hi"),
        AList'[AInt (1), AInt (2)],
        ANull
    ];
end Check;
