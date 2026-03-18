procedure Check is
   X : A_Val := AMap'(
       AEntry ("key\nwith\nnewlines", AStr ("value1")),
       AEntry ("key\twith\ttabs", AStr ("value2")),
       AEntry ("", AStr ("value3"))
   );
begin
   null;
end Check;
