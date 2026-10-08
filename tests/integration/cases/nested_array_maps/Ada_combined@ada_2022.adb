with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("groups", AList'[AList'[AMap'[AEntry ("id", AInt (1))]], AList'[AMap'[AEntry ("id", AInt (2))]]])
    ];
begin
    my_data := AMap'[
        AEntry ("groups", AList'[AList'[AMap'[AEntry ("id", AInt (1))]], AList'[AMap'[AEntry ("id", AInt (2))]]])
    ];
end Main;
