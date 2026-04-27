procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AFloat (1.0 / 0.0),
            AFloat (-1.0 / 0.0),
            AFloat (0.0 / 0.0)
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AFloat (1.0 / 0.0),
            AFloat (-1.0 / 0.0),
            AFloat (0.0 / 0.0)
        );
    end Check_Assignment;
begin
    null;
end Check;
