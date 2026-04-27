procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            ABool (True),
            ABool (False),
            ABool (True)
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            ABool (True),
            ABool (False),
            ABool (True)
        );
    end Check_Assignment;
begin
    null;
end Check;
