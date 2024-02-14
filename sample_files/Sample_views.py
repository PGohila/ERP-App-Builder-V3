
def <**screen_name**>(request):
    records=<**model_name**>.objects.all()
    form=<**model_name**>Form()
    if request.method=="POST":
        form=<**model_name**>Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Saved Successfully')
            return redirect('<**screen_name**>')
        else:
            messages.warning(request, form.errors)
    context={
        'form':form,'records':records,
    }
    return render(request,'<**screen_name**>.html',context)




def <**screen_name**>_view(request,pk):
    records=<**model_name**>.objects.all()
    record=<**model_name**>.objects.get(id=pk)
    form=<**model_name**>Form(instance=record)
    context={
        'records':records, 'form':form, 'view':True
    }
    return render(request,"<**screen_name**>.html",context)

def <**screen_name**>_edit(request,pk):
    records=<**model_name**>.objects.all()
    record=<**model_name**>.objects.get(id=pk)
    form=<**model_name**>Form(instance=record)
    if request.method=="POST":
        form=<**model_name**>Form(request.POST,instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Updated Successfully')
            return redirect('<**screen_name**>')
        else:
            messages.warning(request, form.errors)
    context={
        'form':form,'records':records,"edit":True
    }
    return render(request, '<**screen_name**>.html', context)

def <**screen_name**>_delete(request,pk):
    records=<**model_name**>.objects.get(id=pk)
    records.delete()
    messages.success(request, 'Record Deleted Successfully')
    return redirect('<**screen_name**>')