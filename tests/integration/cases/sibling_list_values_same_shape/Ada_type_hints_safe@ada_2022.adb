with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("test", AList'[AInt (5), AList'[AStr ("compile"), AStr ("test")]]),
        AEntry ("package", AList'[AInt (7), AList'[AStr ("link"), AStr ("test")]])
    ];
begin
    null;
end Main;
