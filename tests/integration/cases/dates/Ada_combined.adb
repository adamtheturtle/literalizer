procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("date", AStr ("2024-01-15")),
            AEntry ("datetime", AStr ("2024-01-15T12:30:00+00:00"))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("date", AStr ("2024-01-15")),
            AEntry ("datetime", AStr ("2024-01-15T12:30:00+00:00"))
        );
    end Check_Assignment;
begin
    null;
end Check;
