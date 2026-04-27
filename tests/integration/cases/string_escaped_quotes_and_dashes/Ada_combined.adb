with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AStr ("hello ""world"" -- not a comment");
begin
    my_data := AStr ("hello ""world"" -- not a comment");
end Check;
