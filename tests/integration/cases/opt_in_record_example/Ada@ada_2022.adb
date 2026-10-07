with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("name", AStr ("Ada")),
        AEntry ("active", ABool (True)),
        AEntry ("scores", AList'[AInt (1), AInt (2), AInt (3)])
    ];
begin
    null;
end Main;
