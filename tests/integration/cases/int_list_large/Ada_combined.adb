procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AInt (1000000),
            AInt (-1234),
            AInt (255),
            AInt (-10)
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AInt (1000000),
            AInt (-1234),
            AInt (255),
            AInt (-10)
        );
    end Check_Assignment;
begin
    null;
end Check;
