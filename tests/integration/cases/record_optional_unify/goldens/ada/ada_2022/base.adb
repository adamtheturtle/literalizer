with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("items", AList'[AMap'[AEntry ("id", AInt (1))], AMap'[AEntry ("id", AInt (2)), AEntry ("count", AInt (10))], AMap'[AEntry ("id", AInt (3)), AEntry ("count", AInt (20))]])
    ];
begin
    null;
end Main;
