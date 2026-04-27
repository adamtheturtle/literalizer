procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("description", AStr ("# not a comment" & Character'Val(10))),
            AEntry ("name", AStr ("foo"))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("description", AStr ("# not a comment" & Character'Val(10))),
            AEntry ("name", AStr ("foo"))
        );
    end Check_Assignment;
begin
    null;
end Check;
