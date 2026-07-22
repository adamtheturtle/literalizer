with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("missing", ANull), AEntry ("present", AInt (1))],
        AMap'[AEntry ("missing", AInt (2)), AEntry ("present", AInt (3))]
    ];
begin
    my_data := AList'[
        AMap'[AEntry ("missing", ANull), AEntry ("present", AInt (1))],
        AMap'[AEntry ("missing", AInt (2)), AEntry ("present", AInt (3))]
    ];
end Main;
