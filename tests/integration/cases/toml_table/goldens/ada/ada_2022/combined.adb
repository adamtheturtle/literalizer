with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("section", AMap'[AEntry ("value", AInt (1))])
    ];
begin
    my_data := AMap'[
        AEntry ("section", AMap'[AEntry ("value", AInt (1))])
    ];
end Main;
