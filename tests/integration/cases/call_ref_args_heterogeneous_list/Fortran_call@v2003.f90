module fval_m
  implicit none
  integer, parameter :: int64 = selected_int_kind(18)
  type :: fval_t
    integer :: t = 0
  end type fval_t
contains
  function fnull() result(v); type(fval_t) :: v; end function
  function fbool(b) result(v); logical, intent(in) :: b; type(fval_t) :: v; end function
  function fint(n) result(v); integer(kind=int64), intent(in) :: n; type(fval_t) :: v; end function
  function freal(x) result(v); real, intent(in) :: x; type(fval_t) :: v; end function
  function fstr(s) result(v); character(len=*), intent(in) :: s; type(fval_t) :: v; end function
  function flist(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function fmap(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function fset(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function fentry(k, u) result(v); character(len=*), intent(in) :: k; type(fval_t), intent(in) :: u; type(fval_t) :: v; end function
end module fval_m
program main
    use fval_m
    implicit none
    type(fval_t) :: my_ints
    type(fval_t) :: my_strings
    type(fval_t) :: my_empty
    my_ints = flist([fval_t :: &
        fint(1_int64), &
        fint(2_int64), &
        fint(3_int64) &
    ])
    my_strings = flist([fval_t :: &
        fstr('a'), &
        fstr('b') &
    ])
    my_empty = flist([fval_t :: ])
    call process(my_ints, fint(42_int64))
    call process(my_strings, fint(7_int64))
    call process(my_empty, fint(99_int64))
contains
    subroutine process(data, count)
        implicit none
        type(fval_t), intent(in) :: data, count
    end subroutine process
end program main
