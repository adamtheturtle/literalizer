with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("rows", AList'[AMap'[AEntry ("replacement", ANull), AEntry ("present", AInt (1))], AMap'[AEntry ("replacement", AInt (2)), AEntry ("present", AInt (3))]])
    ];
begin
    my_data := AMap'[
        AEntry ("rows", AList'[AMap'[AEntry ("replacement", ANull), AEntry ("present", AInt (1))], AMap'[AEntry ("replacement", AInt (2)), AEntry ("present", AInt (3))]])
    ];
end Main;
