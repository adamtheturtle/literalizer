with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AMap'[AEntry ("k", AInt (2208988800))]),
        AEntry ("b", AMap'[AEntry ("k", AInt (1))])
    ];
begin
    null;
end Main;
