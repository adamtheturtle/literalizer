with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        AEntry ("name", AStr ("Alice")),
        AEntry ("scores", AList'[AInt (10), AInt (20), AInt (30)])
    ];
begin
    null;
end Check;
