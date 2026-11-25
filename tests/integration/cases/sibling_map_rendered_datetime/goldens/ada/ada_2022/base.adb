with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AMap'[AEntry ("k", AStr ("2020-01-01T00:00:00+00:00"))]),
        AEntry ("b", AMap'[AEntry ("k", AStr ("string"))])
    ];
begin
    null;
end Main;
