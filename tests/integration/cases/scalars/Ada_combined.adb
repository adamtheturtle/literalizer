procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AInt (42),
            AFloat (3.14),
            ABool (True),
            ABool (False),
            AStr ("hello ""world""")
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AInt (42),
            AFloat (3.14),
            ABool (True),
            ABool (False),
            AStr ("hello ""world""")
        );
    end Check_Assignment;
begin
    null;
end Check;
