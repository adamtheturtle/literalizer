with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("s", AInt (1))],
        AMap'[AEntry ("t", AInt (3))]
    ];
begin
    null;
end Main;
