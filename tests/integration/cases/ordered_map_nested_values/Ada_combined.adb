procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("name", AStr ("Alice")),
            AEntry ("scores", AMap'(AEntry ("1", AStr ("first")), AEntry ("2", AStr ("second"))))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("name", AStr ("Alice")),
            AEntry ("scores", AMap'(AEntry ("1", AStr ("first")), AEntry ("2", AStr ("second"))))
        );
    end Check_Assignment;
begin
    null;
end Check;
