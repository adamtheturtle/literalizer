procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AStr ("2024-01-15T12:30:00.123456+00:00"),
            AStr ("2024-06-01T08:00:00+00:00")
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AStr ("2024-01-15T12:30:00.123456+00:00"),
            AStr ("2024-06-01T08:00:00+00:00")
        );
    end Check_Assignment;
begin
    null;
end Check;
