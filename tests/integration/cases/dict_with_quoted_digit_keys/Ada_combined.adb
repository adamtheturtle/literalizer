with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("0a", AStr ("first")),
        AEntry ("1b", AStr ("second"))
    ];
begin
    my_data := AMap'[
        AEntry ("0a", AStr ("first")),
        AEntry ("1b", AStr ("second"))
    ];
end Main;
