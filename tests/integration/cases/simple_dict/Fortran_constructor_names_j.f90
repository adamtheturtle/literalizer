module fval_m
  use, intrinsic :: iso_fortran_env, only: int64
  implicit none
  type :: fval_t
    integer :: t = 0
  end type fval_t
contains
  function jnull() result(v); type(fval_t) :: v; end function
  function jbool(b) result(v); logical, intent(in) :: b; type(fval_t) :: v; end function
  function jint(n) result(v); integer(kind=int64), intent(in) :: n; type(fval_t) :: v; end function
  function jreal(x) result(v); real, intent(in) :: x; type(fval_t) :: v; end function
  function jstr(s) result(v); character(len=*), intent(in) :: s; type(fval_t) :: v; end function
  function jlist(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function jmap(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function jset(a) result(v); type(fval_t), intent(in) :: a(:); type(fval_t) :: v; end function
  function jentry(k, u) result(v); character(len=*), intent(in) :: k; type(fval_t), intent(in) :: u; type(fval_t) :: v; end function
end module fval_m
program main
    use fval_m
    implicit none
    type(fval_t) :: my_data
    my_data = jmap([fval_t :: &
        jentry('name', jstr('Alice')), &
        jentry('age', jint(30_int64)), &
        jentry('active', jbool(.true.)), &
        jentry('score', jnull()) &
    ])
end program main
