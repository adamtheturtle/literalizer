with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        AEntry ("a", AMap'[AEntry ("x", AInt (1))]),
        AEntry ("b", AInt (2))
    ];
begin
    my_data := AMap'[
        AEntry ("a", AMap'[AEntry ("x", AInt (1))]),
        AEntry ("b", AInt (2))
    ];
end Check;
