with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        AEntry ("key", AStr ("it's here"))  -- a comment
    ];
begin
    null;
end Check;
