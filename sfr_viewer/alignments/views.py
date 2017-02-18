from django.shortcuts import render_to_response, get_object_or_404, render
from swmmio import swmmio
from swmmio.damage import parcels
from swmmio.reporting import visualize
from swmmio.reporting.reporting import FloodReport, ComparisonReport, read_report_dir
from pyplan.helpers import id_possible_next_phases
from pyplan import BenefitCost, plots
import geojson
import os
import pandas as pd
from .models import SFRPhase
import plotly.graph_objs as go
from .generate_plots import next_phases_scatter
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
resultsfile = os.path.join(ADMIN_DIR, 'raw_results.csv')
bc = BenefitCost(resultsfile, benefit_col='Eliminated', cost_col='Cost')
proj_ids = bc.raw_data.Option_ID.tolist()
proj_codes = bc.project_codes #e.g. [M, W, R]


# Create your views here.


def phase_view(request, alignmenta, alignmentb):

    #grab the current phase and the previous phase
    phase_existing = get_object_or_404(SFRPhase, slug=alignmenta)
    phase_proposed = get_object_or_404(SFRPhase, slug=alignmentb)

    #get the report directories, create report objects
    rpt_dir_ex = os.path.join(phase_existing.data_directory, 'Report')
    rpt_dir_pr = os.path.join(phase_proposed.data_directory, 'Report')
    rpt_ex = read_report_dir(rpt_dir_ex)
    rpt_pr = read_report_dir(rpt_dir_pr)

    #grab the geojson data
    # with open (os.path.join(rpt_dir_ex, 'new_conduits.json'),'r') as f:
    #     geo_ex = geojson.loads(f.read())
    # with open (os.path.join(rpt_dir_pr, 'new_conduits.json'), 'r') as f:
    #     geo_pr = geojson.loads(f.read())
    # with open (r"C:\Users\Adam.Erispaha\Downloads\Political_Divisions.geojson",'r') as f:
    #     ward = geojson.loads(f.read())

    #COST CALCS
    ex_cost = rpt_ex.cost_estimate #pd.read_csv(os.path.join(rpt_dir_ex, 'cost_estimate.csv'))
    pr_cost = rpt_pr.cost_estimate #pd.read_csv(os.path.join(rpt_dir_pr, 'cost_estimate.csv'))
    inc_cost = pr_cost - ex_cost #pr_cost.TotalCostEstimate.sum() - ex_cost.TotalCostEstimate.sum()

    #PARCEL CALCS (benefits)
    print 'reading parcel data'
    #read the report from the report directory
    # parc_pr = read_report_dir(rpt_dir_pr).parcel_flooding#, 'parcel_flood_comparison.csv'), index_col=0)
    # parc_ex = read_report_dir(rpt_dir_ex).parcel_flooding#rpt_dir_ex, 'parcel_flood_comparison.csv'), index_col=0)
    # parc_pr_decr = len(parc_pr.loc[parc_pr.Category=='decreased_flooding'])
    # parc_pr_elim = len(parc_pr.loc[parc_pr.Category=='eliminated_flooding'])
    # parc_pr_incr = len(parc_pr.loc[parc_pr.Category=='increased_flooding'])
    # parc_pr_new =  len(parc_pr.loc[parc_pr.Category=='new_flooding'])
    benefit_inc = rpt_ex.parcel_hrs_flooded - rpt_pr.parcel_hrs_flooded
    benefit_tot = - rpt_pr.parcel_flooding.DeltaHours.sum()

    print 'done parcels'



    #identify the possible next phases of implementation
    next_candidates = id_possible_next_phases(str(alignmentb),proj_codes,proj_ids)
    nxt_phases = [get_object_or_404(SFRPhase, slug=ph) for ph in next_candidates]


    phases = {}
    for ph in [phase_existing, phase_proposed] + nxt_phases:

        rpt_dir = os.path.join(ph.data_directory, 'Report')
        geo = os.path.join(rpt_dir, 'new_conduits.json')
        costdf = pd.read_csv(os.path.join(rpt_dir, 'cost_estimate.csv'))
        phases.update({ph.title:{
            'geo':geo,
            'costdf':costdf,
        }})


    #create the plotly figure
    fig = next_phases_scatter(alignmentb, bc, next_candidates, resultsfile)

    return render(request, 'alignments/phase_view.html', {

            'figure':fig,
            'nxt_phases':nxt_phases,
            'phases':phases,
            'phase_existing':phase_existing,
            'phase_proposed':phase_proposed,
            'geo_ex':rpt_ex.new_conduits_geojson,
            'geo_pr':rpt_pr.new_conduits_geojson,
            'ex_cost':ex_cost,
            'pr_cost':pr_cost,
            'inc_cost':inc_cost,
            'benefit_inc':benefit_inc,
            'benefit_tot':benefit_tot,
            # 'ward':ward
            # 'parc_pr_decr':parc_pr_decr,
            # 'parc_pr_elim':parc_pr_elim,
            # 'parc_pr_incr':parc_pr_incr,
            # 'parc_pr_new':parc_pr_new,
            # 'parc_inc_decr':phase_proposed.flood_improved_parcels - phase_existing.flood_improved_parcels,
            # 'parc_inc_elim':phase_proposed.flood_eliminated_parcels - phase_existing.flood_eliminated_parcels,
            # 'parc_inc_incr':0,
            # 'parc_inc_new':0,#phase_proposed.flood_new_parcels - phase_existing.flood_new_parcels,

        })


def index(request, alignment):


    phase = get_object_or_404(SFRPhase, slug=alignment)

    project_dir = r'P:\02_Projects\SouthPhila\SE_SFR\MasterModels'
    #check if geojson has been created, generate it if not
    geopath = os.path.join(phase.data_directory, 'shapefiles', alignment+'.json')
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
    next_phase_candidates = id_possible_next_phases(str(alignment),
                                                       bc.project_codes,
                                                       bc.raw_data.Option_ID.tolist())
    nxt_phases = [get_object_or_404(SFRPhase, slug=s) for s in next_phase_candidates]


    fig = next_phases_scatter(alignment, bc, next_phase_candidates, resultsfile)

    return render(request, 'alignments/index.html', {
            'alignment': alignment,
            'geodata':geodata,
            'sfrphase':phase,
            'figure':fig,
            'nxt_phases':nxt_phases
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
