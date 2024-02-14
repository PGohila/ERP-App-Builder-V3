# create and view table function
def <**screen_name**>(request):
    form=<**model_name**>Form()
    endpoint = '<**api_endpoint**>/'
    if request.method=="POST":
        form=<**model_name**>Form(request.POST)
        if form.is_valid():
            Output = form.cleaned_data
            for field_name, field in form.fields.items():
                if isinstance(field.widget, forms.DateInput) or isinstance(field, forms.DateField) or isinstance(field, forms.DateTimeField):
                    if Output[field_name]:
                        del Output[field_name]
                        Output[field_name] = request.POST.get(field_name)
            json_data=json.dumps(Output)
            response = call_post_method_for_without_token(BASE_URL,endpoint,json_data)
            if response.status_code not in [200,201]:
                print("error",response)
            else:
                messages.success(request,'Data Successfully Saved', extra_tags="success")
                return redirect('<**screen_name**>')
    else:
        print('errorss',form.errors)
    try:
        # getting data from backend
        records_response = call_get_method_without_token(BASE_URL,endpoint)
        if records_response.status_code not in [200,201]:
            messages.error(request, f"Failed to fetch records. {records_response.json()}", extra_tags="warning")
        else:
            records = records_response.json()
            # You can pass 'records' to your template for rendering
            context = {'form': form, 'records': records}
            return render(request, '<**screen_name**>.html', context)
    except Exception as e:
        print("An error occurred: Expecting value: line 1 column 1 (char 0)")
    context={
        'form':form,
    }
    return render(request,'<**screen_name**>.html',context)


# edit function
def <**screen_name**>_edit(request,pk):
    <**api_endpoint**> = call_get_method_without_token(BASE_URL, f'<**api_endpoint**>/{pk}/')
    
    if <**api_endpoint**>.status_code in [200,201]:
        <**api_endpoint**>_data = <**api_endpoint**>.json()
    else:
        print('error------',<**api_endpoint**>)
        messages.error(request, 'Failed to retrieve data for <**api_endpoint**>. Please check your connection and try again.', extra_tags='warning')
        return redirect('<**screen_name**>')

    if request.method=="POST":
        form=<**model_name**>Form(request.POST, initial=<**api_endpoint**>_data)
        if form.is_valid():
            updated_data = form.cleaned_data
            for field_name, field in form.fields.items():
                if isinstance(field.widget, forms.DateInput) or isinstance(field, forms.DateField) or isinstance(field, forms.DateTimeField):
                    if updated_data[field_name]:
                        del updated_data[field_name]
                        updated_data[field_name] = request.POST.get(field_name)
            # Serialize the updated data as JSON
            json_data = json.dumps(updated_data)
            response = call_put_method_without_token(BASE_URL, f'<**api_endpoint**>/{pk}/', json_data)

            if response.status_code in [200,201]: 
                messages.success(request, 'Your data has been successfully saved', extra_tags='success')
                return redirect('<**screen_name**>') 
            else:
                error_message = response.json()
                messages.error(request, f"Oops..! {error_message}", extra_tags='warning')
        else:
            print("An error occurred: Expecting value: line 1 column 1 (char 0)")
    else:
        form = <**model_name**>Form(initial=<**api_endpoint**>_data)

    context={
        'form':form,
    }
    return render(request,'<**screen_name**>_edit.html',context)

def <**screen_name**>_delete(request,pk):
    end_point = f'<**api_endpoint**>/{pk}/'
    <**api_endpoint**> = call_delete_method_without_token(BASE_URL, end_point)
    if <**api_endpoint**>.status_code not in [200,201]:
        messages.error(request, 'Failed to delete data for <**api_endpoint**>. Please try again.', extra_tags='warning')
        return redirect('<**screen_name**>')
    else:
        messages.success(request, 'Successfully deleted data for <**api_endpoint**>', extra_tags='success')
        return redirect('<**screen_name**>')

