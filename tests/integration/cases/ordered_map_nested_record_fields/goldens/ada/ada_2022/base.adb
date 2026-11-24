with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("first", AMap'[AEntry ("x", AInt (1))]),
        AEntry ("second", AMap'[AEntry ("y", AInt (2))])
    ];
begin
    null;
end Main;
