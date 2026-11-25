with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := ASet'[
        AStr ("apple"),  -- inline comment
        -- before banana
        AStr ("banana")
        -- trailing
    ];
begin
    my_data := ASet'[
        AStr ("apple"),  -- inline comment
        -- before banana
        AStr ("banana")
        -- trailing
    ];
end Main;
