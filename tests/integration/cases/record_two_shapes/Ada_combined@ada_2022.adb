with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("user", AMap'[AEntry ("id", AInt (1)), AEntry ("name", AStr ("Alice"))]),
        AEntry ("project", AMap'[AEntry ("title", AStr ("report")), AEntry ("tags", AList'[AStr ("draft"), AStr ("urgent")])])
    ];
begin
    my_data := AMap'[
        AEntry ("user", AMap'[AEntry ("id", AInt (1)), AEntry ("name", AStr ("Alice"))]),
        AEntry ("project", AMap'[AEntry ("title", AStr ("report")), AEntry ("tags", AList'[AStr ("draft"), AStr ("urgent")])])
    ];
end Main;
