procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AFloat (1.1),
            AFloat (-2.2),
            AFloat (3.3)
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AFloat (1.1),
            AFloat (-2.2),
            AFloat (3.3)
        );
    end Check_Assignment;
begin
    null;
end Check;
