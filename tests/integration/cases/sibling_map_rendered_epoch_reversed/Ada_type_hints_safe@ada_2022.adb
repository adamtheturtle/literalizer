with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("b", AMap'[AEntry ("k", AInt (1))]),
        AEntry ("a", AMap'[AEntry ("k", AStr ("2040-01-01T00:00:00+00:00"))])
    ];
begin
    null;
end Main;
