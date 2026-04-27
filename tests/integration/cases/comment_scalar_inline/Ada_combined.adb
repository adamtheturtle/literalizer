procedure Check is
    procedure Check_Declaration is
        -- note
        my_data : A_Val := AInt (42);
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        -- note
        my_data := AInt (42);
    end Check_Assignment;
begin
    null;
end Check;
