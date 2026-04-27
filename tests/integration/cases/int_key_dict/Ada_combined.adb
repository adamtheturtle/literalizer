procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("1", AStr ("one")),
            AEntry ("2", AStr ("two")),
            AEntry ("42", AStr ("answer"))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("1", AStr ("one")),
            AEntry ("2", AStr ("two")),
            AEntry ("42", AStr ("answer"))
        );
    end Check_Assignment;
begin
    null;
end Check;
