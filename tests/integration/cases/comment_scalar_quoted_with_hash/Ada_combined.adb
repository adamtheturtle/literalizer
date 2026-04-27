procedure Check is
    procedure Check_Declaration is
        -- note
        my_data : A_Val := AStr ("hello # world");
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        -- note
        my_data := AStr ("hello # world");
    end Check_Assignment;
begin
    null;
end Check;
