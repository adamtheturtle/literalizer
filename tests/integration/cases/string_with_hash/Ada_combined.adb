with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AStr ("issue #{42}"),
        AStr ("color #red")
    ];
begin
    my_data := AList'[
        AStr ("issue #{42}"),
        AStr ("color #red")
    ];
end Check;
