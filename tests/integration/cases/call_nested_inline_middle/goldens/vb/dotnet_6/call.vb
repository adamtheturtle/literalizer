Imports System.Collections.Generic
Module Check
    Function f(ops As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        f(New String()() {New String() {"DEL", "b", "10"}, New String() {"ADD", "a", "x"}})  ' note
        ' next call
        f(New String()() {New String() {"ADD", "c", "y"}})
    End Sub
End Module
