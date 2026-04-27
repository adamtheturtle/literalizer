procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("message", AStr ("no comment here"))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("message", AStr ("no comment here"))
        );
    end Check_Assignment;
begin
    null;
end Check;
