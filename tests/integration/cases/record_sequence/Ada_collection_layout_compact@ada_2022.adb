with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("id", AInt (1)), AEntry ("label", AStr ("first")), AEntry ("tags", AList'[])],
        AMap'[AEntry ("id", AInt (2)), AEntry ("label", AStr ("second")), AEntry ("tags", AList'[])],
        AMap'[AEntry ("id", AInt (3)), AEntry ("label", AStr ("third")), AEntry ("tags", AList'[])]
    ];
begin
    null;
end Main;
