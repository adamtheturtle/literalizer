with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        AEntry ("name", AStr ("Alice")),
        AEntry ("age", AInt (30)),
        AEntry ("active", ABool (True)),
        AEntry ("score", ANull)
    ];
begin
    null;
end Check;
