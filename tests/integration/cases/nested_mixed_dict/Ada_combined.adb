with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("outer", AMap'[AEntry ("a", AInt (1)), AEntry ("b", AStr ("x")), AEntry ("c", ANull)])
    ];
begin
    my_data := AMap'[
        AEntry ("outer", AMap'[AEntry ("a", AInt (1)), AEntry ("b", AStr ("x")), AEntry ("c", ANull)])
    ];
end Main;
