with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("first", AStr ("Alice")), AEntry ("last", AStr ("Smith"))],
        AMap'[AEntry ("first", AStr ("Bob")), AEntry ("last", AStr ("Jones"))]
    ];
begin
    null;
end Main;
