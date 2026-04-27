procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := ASet'(
            AStr ("2024-01-15"),
            AStr ("2024-06-01")
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := ASet'(
            AStr ("2024-01-15"),
            AStr ("2024-06-01")
        );
    end Check_Assignment;
begin
    null;
end Check;
