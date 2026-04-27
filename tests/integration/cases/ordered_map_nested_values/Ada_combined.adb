with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        AEntry ("name", AStr ("Alice")),
        AEntry ("scores", AMap'[AEntry ("1", AStr ("first")), AEntry ("2", AStr ("second"))])
    ];
begin
    my_data := AMap'[
        AEntry ("name", AStr ("Alice")),
        AEntry ("scores", AMap'[AEntry ("1", AStr ("first")), AEntry ("2", AStr ("second"))])
    ];
end Check;
