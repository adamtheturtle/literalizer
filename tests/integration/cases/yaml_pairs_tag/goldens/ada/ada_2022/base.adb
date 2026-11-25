with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("first", AInt (1))],
        AMap'[AEntry ("repeated", AStr ("a"))],
        AMap'[AEntry ("repeated", AStr ("b"))]
    ];
begin
    null;
end Main;
