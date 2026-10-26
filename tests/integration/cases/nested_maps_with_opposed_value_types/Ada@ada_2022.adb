with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("input", AMap'[AEntry ("name", AStr ("alice")), AEntry ("city", AStr ("paris"))]), AEntry ("expected", AMap'[AEntry ("count", AInt (1)), AEntry ("total", AInt (2))])],
        AMap'[AEntry ("input", AMap'[AEntry ("name", AInt (10)), AEntry ("city", AInt (20))]), AEntry ("expected", AMap'[AEntry ("count", AStr ("done")), AEntry ("total", AStr ("pending"))])]
    ];
begin
    null;
end Main;
