procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AList'(AFloat (1.5), AFloat (2.5)),
            AList'(AFloat (3.5), AFloat (4.5))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AList'(AFloat (1.5), AFloat (2.5)),
            AList'(AFloat (3.5), AFloat (4.5))
        );
    end Check_Assignment;
begin
    null;
end Check;
