procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            -- first
            AStr ("a"),
            -- second
            AStr ("b")
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            -- first
            AStr ("a"),
            -- second
            AStr ("b")
        );
    end Check_Assignment;
begin
    null;
end Check;
