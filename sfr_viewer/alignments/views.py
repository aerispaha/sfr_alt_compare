from django.shortcuts import render_to_response, get_object_or_404, render
from swmmio import swmmio
from swmmio.damage import parcels
from swmmio.reporting import visualize
from swmmio.reporting.reporting import FloodReport, ComparisonReport, read_report_dir
from pyplan.helpers import id_possible_next_phases
from pyplan import BenefitCost, plots
import geojson, json
import os
import pandas as pd
from .models import Phase
import plotly.graph_objs as go
from .generate_plots import next_phases_scatter, nxt_phase_compare_plt
import math


#project level constants
PROJECT_DIR = r'P:\02_Projects\SouthPhila\SE_SFR\MasterModels'
COMMON_DATA_DIR = os.path.join(PROJECT_DIR, 'CommonData')
ADMIN_DIR = os.path.join(PROJECT_DIR, 'ProjectAdmin')

#instantiate the true baseline flood report
baseline_model = swmmio.Model(os.path.join(PROJECT_DIR, 'Baseline'))
pn_join_csv = os.path.join(COMMON_DATA_DIR,r'pennsport_sheds_parcels_join.csv')
parcel_node_join_df = pd.read_csv(pn_join_csv)
baserpt = FloodReport(baseline_model, parcel_node_join_df)

#BENEFIT COST COMMON DATA
resultsfile = os.path.join(ADMIN_DIR, 'all_parcels_results_170217.csv')
bc = BenefitCost(resultsfile, benefit_col='PARCEL_HRS_REDUCED_DELTA_THRESH',
                 cost_col='Cost')
proj_ids = bc.raw_data.Option_ID.tolist()
proj_codes = bc.project_codes #e.g. [M, W, R]



# Create your views here.
def dashboard(request, phase_slug):
    #grab the current phase and the previous phase
    phase = get_object_or_404(Phase, slug=phase_slug)

    efficiency = phase.parcel_hours_reduced / phase.cost_estimate

    #load the geojson parcel data
    with open (phase.data_file, 'r') as f:
        data = json.loads(f.read())
        parcels = data['parcels']
        delta_parcels = data['delta_parcels']

    #identify the possible next phases of implementation
    next_candidates = id_possible_next_phases(str(phase_slug),proj_codes,proj_ids)
    nxt_phases = [get_object_or_404(Phase, slug=ph) for ph in next_candidates]
    nxt_phase_conduits = {np.slug:np.new_conduits for np in nxt_phases}

    for p in nxt_phases:
        #calculate the incremental stats
        p.inc_cost = p.cost_estimate - phase.cost_estimate
        p.inc_bene = p.parcel_hours_reduced - phase.parcel_hours_reduced
        p.efficiency = p.inc_bene / p.inc_cost

    #create the plotly figure
    # fig = next_phases_scatter(b, bc, next_candidates, resultsfile)

    fig = nxt_phase_compare_plt(phase, nxt_phases)

    return render(request, 'alignments/dashboard.html', {
            # 'figure':fig,
            'phase':phase,
            'efficiency':efficiency,
            'phase_conduits':geojson.dumps(phase.new_conduits),
            'parcels':geojson.dumps(parcels),
            'delta_parcels':geojson.dumps(delta_parcels),
            'nxt_phases':nxt_phases,
            'nxt_phase_conduits':json.dumps(nxt_phase_conduits),
            'fig':fig,
        })
    # return render(request, 'alignments/dashboard.html', {})

def mapbox_view(request, phase_slug):

    #grab the current phase and the previous phase
    phase = get_object_or_404(Phase, slug=phase_slug)

    efficiency = phase.parcel_hours_reduced / phase.cost_estimate

    #load the geojson parcel data
    with open (phase.data_file, 'r') as f:
        data = json.loads(f.read())
        parcels = data['parcels']
        delta_parcels = data['delta_parcels']

    #identify the possible next phases of implementation
    next_candidates = id_possible_next_phases(str(phase_slug),proj_codes,proj_ids)
    nxt_phases = [get_object_or_404(Phase, slug=ph) for ph in next_candidates]
    nxt_phase_conduits = {np.slug:np.new_conduits for np in nxt_phases}

    for p in nxt_phases:
        #calculate the incremental stats
        p.inc_cost = p.cost_estimate - phase.cost_estimate
        p.inc_bene = p.parcel_hours_reduced - phase.parcel_hours_reduced
        p.efficiency = p.inc_bene / p.inc_cost

    #create the plotly figure
    # fig = next_phases_scatter(b, bc, next_candidates, resultsfile)

    fig = nxt_phase_compare_plt(phase, nxt_phases)

    return render(request, 'alignments/mb_view.html', {
            # 'figure':fig,
            'phase':phase,
            'efficiency':efficiency,
            'phase_conduits':geojson.dumps(phase.new_conduits),
            'parcels':geojson.dumps(parcels),
            'delta_parcels':geojson.dumps(delta_parcels),
            'nxt_phases':nxt_phases,
            'nxt_phase_conduits':json.dumps(nxt_phase_conduits),
            'fig':fig,
        })
