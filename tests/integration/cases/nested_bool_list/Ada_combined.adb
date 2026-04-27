procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AList'(ABool (True), ABool (False)),
            AList'(ABool (True), ABool (True))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AList'(ABool (True), ABool (False)),
            AList'(ABool (True), ABool (True))
        );
    end Check_Assignment;
begin
    null;
end Check;
