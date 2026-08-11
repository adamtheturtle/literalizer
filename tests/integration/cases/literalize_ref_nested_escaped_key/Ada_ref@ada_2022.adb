with A_Stub; use A_Stub;
procedure Main is
    foo : A_Val := AMap'[
        AEntry ("_", AStr ("_"))
    ];
    my_data : A_Val := AMap'[
        AEntry ("items", AList'[AMap'[AEntry ("other", AInt (1))], foo]),
        AEntry ("mapping", AMap'[AEntry ("value", foo)])
    ];
begin
    null;
end Main;
