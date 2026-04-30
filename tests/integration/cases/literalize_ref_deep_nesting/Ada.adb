with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AMap'[AEntry ("b", AMap'[AEntry ("c", AMap'[AEntry ("$ref", AStr ("deep"))])])])
    ];
begin
    null;
end Main;
