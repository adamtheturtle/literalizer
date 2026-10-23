with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("metrics", AMap'[AEntry ("count", AInt (100)), AEntry ("rate", AInt (50))]),
        AEntry ("flags", AMap'[AEntry ("retries", AInt (3)), AEntry ("timeout", AInt (30))])
    ];
begin
    null;
end Main;
