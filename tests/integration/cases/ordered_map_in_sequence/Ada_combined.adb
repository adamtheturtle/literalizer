with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AMap'[AEntry ("a", AInt (1))],
        AStr ("hello")
    ];
begin
    my_data := AList'[
        AMap'[AEntry ("a", AInt (1))],
        AStr ("hello")
    ];
end Check;
