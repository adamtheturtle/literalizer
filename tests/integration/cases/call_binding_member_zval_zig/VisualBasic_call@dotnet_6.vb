Module Check
    Class ObjType_0_
        Public Function ZVal(_arg As Object) As Object
            Return Nothing
        End Function
    End Class
    Dim obj As New ObjType_0_()
    Sub _calls()
        Dim my_data = obj.ZVal(42) // note
    End Sub
End Module
