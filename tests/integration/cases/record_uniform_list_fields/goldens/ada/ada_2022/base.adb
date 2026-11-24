with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("scores", AList'[AInt (1), AInt (2)])],
        AMap'[AEntry ("scores", AList'[AInt (3), AInt (4)])]
    ];
begin
    null;
end Main;
