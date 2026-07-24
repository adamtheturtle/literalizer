with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("first", AStr ("Alice")), AEntry ("last", AStr ("Smith"))],
        AMap'[AEntry ("first", AStr ("Bob")), AEntry ("middle", AStr ("Quincy"))]
    ];
begin
    my_data := AList'[
        AMap'[AEntry ("first", AStr ("Alice")), AEntry ("last", AStr ("Smith"))],
        AMap'[AEntry ("first", AStr ("Bob")), AEntry ("middle", AStr ("Quincy"))]
    ];
end Main;
