with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        AEntry ("name", AStr ("Alice")),
        AEntry ("score", ANull),
        AEntry ("age", AInt (30))
    ];
begin
    my_data := AMap'[
        AEntry ("name", AStr ("Alice")),
        AEntry ("score", ANull),
        AEntry ("age", AInt (30))
    ];
end Check;
