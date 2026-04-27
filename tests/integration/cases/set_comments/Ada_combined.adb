procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := ASet'(
            AStr ("apple"),  -- inline comment
            -- before banana
            AStr ("banana")
            -- trailing
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := ASet'(
            AStr ("apple"),  -- inline comment
            -- before banana
            AStr ("banana")
            -- trailing
        );
    end Check_Assignment;
begin
    null;
end Check;
