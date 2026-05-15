with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("scores", AList'[AInt (10), AInt (20), AInt (30)]),
        AEntry ("args", AList'[AInt (1), AStr ("email"), AStr ("a@gmail.com"), AInt (100)])
    ];
begin
    my_data := AMap'[
        AEntry ("scores", AList'[AInt (10), AInt (20), AInt (30)]),
        AEntry ("args", AList'[AInt (1), AStr ("email"), AStr ("a@gmail.com"), AInt (100)])
    ];
end Main;
