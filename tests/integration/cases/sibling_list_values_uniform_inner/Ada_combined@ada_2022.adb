with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("lint", AList'[AInt (2), AList'[AInt (1)]]),
        AEntry ("test", AList'[AInt (5), AList'[AInt (7)]])
    ];
begin
    my_data := AMap'[
        AEntry ("lint", AList'[AInt (2), AList'[AInt (1)]]),
        AEntry ("test", AList'[AInt (5), AList'[AInt (7)]])
    ];
end Main;
