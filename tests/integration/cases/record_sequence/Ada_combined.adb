with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("id", AInt (1)), AEntry ("label", AStr ("first"))],
        AMap'[AEntry ("id", AInt (2)), AEntry ("label", AStr ("second"))],
        AMap'[AEntry ("id", AInt (3)), AEntry ("label", AStr ("third"))]
    ];
begin
    my_data := AList'[
        AMap'[AEntry ("id", AInt (1)), AEntry ("label", AStr ("first"))],
        AMap'[AEntry ("id", AInt (2)), AEntry ("label", AStr ("second"))],
        AMap'[AEntry ("id", AInt (3)), AEntry ("label", AStr ("third"))]
    ];
end Main;
