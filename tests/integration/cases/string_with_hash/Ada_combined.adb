procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AStr ("issue #{42}"),
            AStr ("color #red")
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AStr ("issue #{42}"),
            AStr ("color #red")
        );
    end Check_Assignment;
begin
    null;
end Check;
