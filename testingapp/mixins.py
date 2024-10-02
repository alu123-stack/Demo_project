class PrintUsernameMixin:
    def dispatch(self,*args,**kwargs):
        print("*********************")
        print(self.request.user.username)
        return super().dispatch(*args,**kwargs)
    def execute_view(self):
        print("this view is excecuting")