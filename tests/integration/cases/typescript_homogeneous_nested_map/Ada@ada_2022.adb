with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("first", AMap'[AEntry ("x", AInt (1)), AEntry ("y", AInt (2))]),
        AEntry ("second", AMap'[AEntry ("z", AInt (3))])
    ];
begin
    null;
end Main;
