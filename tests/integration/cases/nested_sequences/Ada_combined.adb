with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AList'[AList'[AInt (1), AInt (2)], AList'[AInt (3), AInt (4)]],
        AList'[AList'[AInt (5)]]
    ];
begin
    my_data := AList'[
        AList'[AList'[AInt (1), AInt (2)], AList'[AInt (3), AInt (4)]],
        AList'[AList'[AInt (5)]]
    ];
end Check;
