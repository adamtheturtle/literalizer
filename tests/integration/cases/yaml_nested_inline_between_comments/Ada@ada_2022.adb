with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[AInt (2), AStr ("hello")],  -- trailing note
        -- next element
        AList'[AInt (3), AStr ("world")]
    ];
begin
    null;
end Main;
