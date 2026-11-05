Imports System.Collections.Generic
Module Check
    Function make_widget(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        make_widget(New Object() {})
    End Sub
End Module
