with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AMap'[AEntry ("x", AInt (1))]),
        AEntry ("b", AInt (2))
    ];
begin
    null;
end Main;
