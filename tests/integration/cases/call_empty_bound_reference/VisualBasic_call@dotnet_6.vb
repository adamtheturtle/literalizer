Imports System.Collections.Generic
Module Check
    Function make_widget(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim items = New Object() {}
        make_widget(items)
    End Sub
End Module
