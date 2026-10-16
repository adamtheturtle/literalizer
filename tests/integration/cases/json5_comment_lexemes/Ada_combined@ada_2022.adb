with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        -- heading
        AEntry ("a", AStr ("single ' // data")),
        AEntry ("b", AStr ("linecontinuation")),
        AEntry ("c", AStr ("\")),  -- actual comment
        AEntry ("d", AStr (Character'Val(226) & Character'Val(128) & Character'Val(168) & Character'Val(226) & Character'Val(128) & Character'Val(169)))  -- final comment
    ];
begin
    my_data := AMap'[
        -- heading
        AEntry ("a", AStr ("single ' // data")),
        AEntry ("b", AStr ("linecontinuation")),
        AEntry ("c", AStr ("\")),  -- actual comment
        AEntry ("d", AStr (Character'Val(226) & Character'Val(128) & Character'Val(168) & Character'Val(226) & Character'Val(128) & Character'Val(169)))  -- final comment
    ];
end Main;
