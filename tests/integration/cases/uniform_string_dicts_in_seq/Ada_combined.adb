with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AMap'[AEntry ("first", AStr ("Alice")), AEntry ("last", AStr ("Smith"))],
        AMap'[AEntry ("first", AStr ("Bob")), AEntry ("last", AStr ("Jones"))]
    ];
begin
    my_data := AList'[
        AMap'[AEntry ("first", AStr ("Alice")), AEntry ("last", AStr ("Smith"))],
        AMap'[AEntry ("first", AStr ("Bob")), AEntry ("last", AStr ("Jones"))]
    ];
end Check;
