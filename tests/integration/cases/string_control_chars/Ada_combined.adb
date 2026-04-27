procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AStr ("line1" & Character'Val(13) & Character'Val(10) & "line2"),
            AStr ("line1" & Character'Val(13) & "line2"),
            AStr (Character'Val(1))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AStr ("line1" & Character'Val(13) & Character'Val(10) & "line2"),
            AStr ("line1" & Character'Val(13) & "line2"),
            AStr (Character'Val(1))
        );
    end Check_Assignment;
begin
    null;
end Check;
