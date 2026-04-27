procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            -- line 1
            -- line 2
            AStr ("a")
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            -- line 1
            -- line 2
            AStr ("a")
        );
    end Check_Assignment;
begin
    null;
end Check;
