from models import SFRPhase, Phase
import os, json
from itertools import chain
from swmmio import swmmio
from swmmio.version_control import utils as vc_utils
import pandas as pd


project_dir = r'P:\02_Projects\SouthPhila\SE_SFR\MasterModels'
baselinedir = os.path.join('Baseline')
paths = tuple(os.path.join(project_dir, x) for x in ['Combinations', 'Segments'])

#read the cost estimate file
# results_fname = 'raw_results.csv'
# raw_res = pd.read_csv(os.path.join(project_dir, 'ProjectAdmin', results_fname))

for path, dirs, files in chain.from_iterable(os.walk(path) for path in paths):
    for f in files:
        if '.inp' in f:
            inp_path = os.path.join(path, f)
            alt = swmmio.Model(inp_path)

            #find the name of the latest build instructions file
            vcdir = os.path.join(alt.inp.dir, 'vc')
            vid = os.path.splitext(os.path.basename(vc_utils.newest_file(vcdir)))[0]

            #load json
            datafile = os.path.join(alt.inp.dir, 'Report_AllParcels', 'rpt.json')
            with open (datafile, 'r') as f:
                rawdata = json.loads(f.read())

            # phase = SFRPhase(
            #     slug = alt.name,
            #     data_directory = alt.inp.dir,
            #     data_file = os.path.join(alt.inp.dir, 'Report_AllParcels', 'rpt.json')
            #     cost_estimate = float(raw_res.loc[raw_res.Option_ID==alt.name, 'Cost']),
            #     flood_eliminated_parcels = float(raw_res.loc[raw_res.Option_ID==alt.name, 'Eliminated']),
            #     flood_improved_parcels = float(raw_res.loc[raw_res.Option_ID==alt.name, 'Improved']),
            #     flood_increased_parcels = float(raw_res.loc[raw_res.Option_ID==alt.name, 'Worse']),
            #     flood_new_parcels = float(raw_res.loc[raw_res.Option_ID==alt.name, 'New']),
            # )
            print 'saving {}'.format(alt.name)
            phase = Phase(
                slug = alt.name,
                data_directory = alt.inp.dir,
                data_file = datafile,
                new_conduits = rawdata['new_conduits'],
                # parcels = rawdata['parcels'],
                # delta_parcels = rawdata['delta_parcels'],
                cost_estimate = rawdata['cost_estimate'],
                parcel_hours_reduced = rawdata['parcel_hours_reduced'],
                parcel_hours_increased =rawdata['parcel_hours_increased'],
                parcel_hours_new = rawdata['parcel_hours_new'],
                sewer_miles_new = rawdata['sewer_miles_new'],
                description = rawdata['description'],
            )

            phase.save()
