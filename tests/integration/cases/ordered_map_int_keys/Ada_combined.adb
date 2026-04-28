with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("1", AStr ("one")),
        AEntry ("2", AStr ("two")),
        AEntry ("42", AStr ("answer"))
    ];
begin
    my_data := AMap'[
        AEntry ("1", AStr ("one")),
        AEntry ("2", AStr ("two")),
        AEntry ("42", AStr ("answer"))
    ];
end Main;
