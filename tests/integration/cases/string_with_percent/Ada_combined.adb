procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AStr ("100% done"),
            AStr ("%(name) is here")
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AStr ("100% done"),
            AStr ("%(name) is here")
        );
    end Check_Assignment;
begin
    null;
end Check;
