with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("name", AStr ("Alice")), AEntry ("age", AInt (30))],
        AMap'[AEntry ("name", AStr ("Bob")), AEntry ("age", AInt (25))]
    ];
begin
    null;
end Main;
