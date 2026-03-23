procedure Check is
   X : A_Val := AMap'(
       AEntry ("key", AStr ("value "" # not a comment"))  -- real
   );
begin
   null;
end Check;
