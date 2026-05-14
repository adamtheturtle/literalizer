with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("key", AStr ("hello   world")), AEntry ("value", AInt (1))]
    ];
begin
    my_data := AList'[
        AMap'[AEntry ("key", AStr ("hello   world")), AEntry ("value", AInt (1))]
    ];
end Main;
