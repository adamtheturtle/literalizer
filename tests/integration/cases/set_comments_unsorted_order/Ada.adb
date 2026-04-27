with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := ASet'[
        -- before apple
        AStr ("apple"),
        AStr ("banana")  -- banana inline
        -- trailing
    ];
begin
    null;
end Check;
