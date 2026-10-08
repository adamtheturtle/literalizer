with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("url", AStr ("https://example.org/a/*b*/")),
        AEntry ("count", AInt (2))
    ];
begin
    null;
end Main;
