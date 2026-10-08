Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process(1)  ' note<U+2028>still commented<U+2029>done
    End Sub
End Module
