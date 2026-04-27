procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AStr ("a"),  -- note a
            AStr ("b")  -- note b
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AStr ("a"),  -- note a
            AStr ("b")  -- note b
        );
    end Check_Assignment;
begin
    null;
end Check;
