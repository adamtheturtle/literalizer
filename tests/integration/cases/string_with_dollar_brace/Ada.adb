procedure Check is
    my_data : A_Val := AList'(
        AStr ("prefix ${HOME} suffix"),
        AStr ("${interpolated}")
    );
begin
    null;
end Check;
