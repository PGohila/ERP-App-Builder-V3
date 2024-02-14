
class SignupForm(ModelForm):
	class Meta:
		model = signup
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs["class"] = "form-control"

class SignupForm(ModelForm):
	class Meta:
		model = signup
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs["class"] = "form-control"

class SignupForm(ModelForm):
	class Meta:
		model = signup
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs["class"] = "form-control"

class SignupForm(ModelForm):
	class Meta:
		model = signup
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs["class"] = "form-control"

class NewForm(ModelForm):
	class Meta:
		model = new
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super(NewForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs["class"] = "form-control"

class NewForm(ModelForm):
	class Meta:
		model = new
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super(NewForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs["class"] = "form-control"

class NewForm(ModelForm):
	class Meta:
		model = new
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super(NewForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs["class"] = "form-control"

class Table1Form(ModelForm):
	class Meta:
		model = table1
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super(Table1Form, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs["class"] = "form-control"
