procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AStr ("2024-01-15"),
            AStr ("2024-02-20")
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AStr ("2024-01-15"),
            AStr ("2024-02-20")
        );
    end Check_Assignment;
begin
    null;
end Check;
