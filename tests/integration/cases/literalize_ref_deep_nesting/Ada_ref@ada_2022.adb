with A_Stub; use A_Stub;
procedure Main is
    deep : A_Val := AMap'[
        AEntry ("_", AStr ("_"))
    ];
    my_data : A_Val := AMap'[
        AEntry ("a", AMap'[AEntry ("b", AMap'[AEntry ("c", deep)])])
    ];
begin
    null;
end Main;
