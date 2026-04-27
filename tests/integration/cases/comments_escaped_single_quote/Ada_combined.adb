procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("key", AStr ("it's here"))  -- a comment
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("key", AStr ("it's here"))  -- a comment
        );
    end Check_Assignment;
begin
    null;
end Check;
