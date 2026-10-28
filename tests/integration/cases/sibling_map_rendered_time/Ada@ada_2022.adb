with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AMap'[AEntry ("k", AStr ("07:30:00"))]),
        AEntry ("b", AMap'[AEntry ("k", AStr ("string"))])
    ];
begin
    null;
end Main;
