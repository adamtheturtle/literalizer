with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("k", AStr ("2040-01-01T00:00:00+00:00"))],
        AMap'[AEntry ("k", AInt (1))]
    ];
begin
    null;
end Main;
