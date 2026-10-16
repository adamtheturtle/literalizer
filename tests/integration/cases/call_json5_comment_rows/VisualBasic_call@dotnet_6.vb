Imports System.Collections.Generic
Module Check
    Function f(a As Object, b As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        ' calls heading
        ' before call one
        ' first argument
        f(1, 2)  ' after call one
        ' second argument
        f(3, 4)
        ' after all calls
    End Sub
End Module
