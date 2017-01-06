from django.shortcuts import render_to_response, get_object_or_404, render
import plots

# Create your views here.
def index(request):

    #return the plot
    data_path = r"F:\code\swmmio_tests\161207\ProjectAdmin\raw_results.csv"
    fig = plots.implementation_sequence(data_path)


    return render(request, 'costcompare/home.html', {
            'figure': fig,
        })
