procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("my-key", AStr ("value1")),
            AEntry ("another-key", AStr ("value2")),
            AEntry ("normal_key", AStr ("value3"))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("my-key", AStr ("value1")),
            AEntry ("another-key", AStr ("value2")),
            AEntry ("normal_key", AStr ("value3"))
        );
    end Check_Assignment;
begin
    null;
end Check;
