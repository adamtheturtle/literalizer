procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AInt (-- note
        42);
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AInt (-- note
        42);
    end Check_Assignment;
begin
    null;
end Check;
