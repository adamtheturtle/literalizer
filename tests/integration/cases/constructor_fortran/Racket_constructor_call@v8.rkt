module constructor_types
  implicit none
  type fval_t
    integer :: value
  end type
contains
  function Playlist() result(value)
    type(fval_t) :: value
    value%value = 42
  end function
end module

program constructor_binding
  use constructor_types
  implicit none
(define p (Playlist))
if (p%value /= 42) stop 1
end program
