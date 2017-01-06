from django.shortcuts import render_to_response, get_object_or_404, render
from swmmio import swmmio
from swmmio.reporting import visualize
from pyplan.helpers import identify_possible_next_ops
from pyplan import BenefitCost
import geojson
import os
import pandas as pd
from .models import SFRPhase

# Create your views here.
def index(request, alignment):


    phase = get_object_or_404(SFRPhase, slug=alignment)

    project_dir = r'P:\02_Projects\SouthPhila\SE_SFR\MasterModels'
    # align_dir = os.path.join(project_dir, 'Combinations', alignment)
    align_dir = phase.data_directory

    #check if geojson has been created, generate it if not
    geopath = os.path.join(align_dir, 'shapefiles', alignment+'.json')
    if os.path.exists(geopath):
        with open(geopath, 'r') as f:
            geodata = geojson.loads(f.read())
    else:
        baseline = swmmio.Model(os.path.join(project_dir, 'Baseline'))
        alt = swmmio.Model(os.path.join(project_dir, 'Combinations', alignment))
        geodata = visualize.create_map(baseline, alt, return_data=True)

        #write to file for next time
        with open (geopath, 'wb') as f:
            f.write(geojson.dumps(geodata))

    #determine the candidates for a next phase of implementation
    resultsfile = os.path.join(project_dir, 'ProjectAdmin', 'raw_results.csv')
    bc = BenefitCost(resultsfile, id_col='Option_ID', benefit_col='Eliminated',
                     cost_col='Cost')
    next_phase_candidates = identify_possible_next_ops(str(alignment),
                                                       bc.project_codes,
                                                       bc.raw_data.Option_ID.tolist())


    return render(request, 'alignments/index.html', {
            'alignment': alignment,
            'geodata':geodata,
            'next_phase_candidates':next_phase_candidates,
            'sfrphase':phase,
        })

def compare(request, alignmenta, alignmentb):
    phase_a = get_object_or_404(SFRPhase, slug=alignmenta)
    phase_b = get_object_or_404(SFRPhase, slug=alignmentb)
    phases = [phase_a, phase_b]
    geos = []
    for p in phases:

        align_dir = p.data_directory
        geopath = os.path.join(align_dir, 'shapefiles', p.slug+'.json')

        with open(geopath, 'r') as f:
            geos.append(geojson.loads(f.read()))

    compare_title = ' vs '.join([p.title for p in phases])
    print geos[1].keys()
    return render(request, 'alignments/compare.html', {
            'geo1':geos[0],
            'geo2':geos[1],
            'phases':phases,
            'compare_title':compare_title
        })
