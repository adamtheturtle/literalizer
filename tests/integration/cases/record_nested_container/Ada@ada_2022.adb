with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("title", AStr ("report")),
        AEntry ("tags", AList'[AStr ("draft"), AStr ("urgent"), AStr ("review")]),
        AEntry ("priority", AInt (2))
    ];
begin
    null;
end Main;
