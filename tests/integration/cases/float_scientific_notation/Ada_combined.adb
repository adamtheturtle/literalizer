procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AFloat (0.0),
            AFloat (1.0),
            AFloat (1500.0),
            AFloat (0.001)
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AFloat (0.0),
            AFloat (1.0),
            AFloat (1500.0),
            AFloat (0.001)
        );
    end Check_Assignment;
begin
    null;
end Check;
