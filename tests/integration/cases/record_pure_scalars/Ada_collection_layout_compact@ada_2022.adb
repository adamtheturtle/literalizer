with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("name", AStr ("Alice")),
        AEntry ("age", AInt (30)),
        AEntry ("active", ABool (True)),
        AEntry ("score", AFloat (4.5))
    ];
begin
    null;
end Main;
