with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("id", AInt (1)),
        AEntry ("owner", AMap'[AEntry ("name", AStr ("Alice")), AEntry ("age", AInt (30))])
    ];
begin
    null;
end Main;
