procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            -- Configuration
            AEntry ("name", AStr ("app")),
            -- Port setting
            AEntry ("port", AInt (3000))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            -- Configuration
            AEntry ("name", AStr ("app")),
            -- Port setting
            AEntry ("port", AInt (3000))
        );
    end Check_Assignment;
begin
    null;
end Check;
