with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("name", AStr ("Alice")),
        AEntry ("scores", AList'[AInt (10), AInt (20), AInt (30)])
    ];
begin
    my_data := AMap'[
        AEntry ("name", AStr ("Alice")),
        AEntry ("scores", AList'[AInt (10), AInt (20), AInt (30)])
    ];
end Main;
