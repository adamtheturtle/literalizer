with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("replacement", AInt (-1)), AEntry ("present", AInt (1))],
        AMap'[AEntry ("replacement", AInt (2)), AEntry ("present", AInt (3))]
    ];
begin
    null;
end Main;
