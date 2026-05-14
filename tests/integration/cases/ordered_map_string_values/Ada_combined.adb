with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("first", AStr ("one")),
        AEntry ("second", AStr ("two")),
        AEntry ("third", AStr ("three"))
    ];
begin
    my_data := AMap'[
        AEntry ("first", AStr ("one")),
        AEntry ("second", AStr ("two")),
        AEntry ("third", AStr ("three"))
    ];
end Main;
