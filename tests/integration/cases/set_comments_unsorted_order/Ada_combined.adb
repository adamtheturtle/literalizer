procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := ASet'(
            -- before apple
            AStr ("apple"),
            AStr ("banana")  -- banana inline
            -- trailing
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := ASet'(
            -- before apple
            AStr ("apple"),
            AStr ("banana")  -- banana inline
            -- trailing
        );
    end Check_Assignment;
begin
    null;
end Check;
