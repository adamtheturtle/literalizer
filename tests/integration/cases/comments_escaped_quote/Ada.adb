procedure Check is
    my_data : A_Val := AMap'(
        AEntry ("key", AStr ("value "" # not a comment"))  -- real
    );
begin
    null;
end Check;
