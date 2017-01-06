import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from pyplan import Sequence, plots

def implementation_sequence(csv_path, bc='Eliminated'):

    raw_data = r"P:\02_Projects\SouthPhila\SE_SFR\MasterModels\ProjectAdmin\raw_results.csv"

    #overall most efficient sequence
    best = Sequence(raw_data, benefit_col=bc, name='Most Efficient')
    r_start = Sequence(raw_data, benefit_col=bc, start_sequence=['R01'],
                       name='Oregon Start')
    w_start = Sequence(raw_data, benefit_col=bc, start_sequence=['W01'],
                       name='Weccacoe Start')
    m_start = Sequence(raw_data, benefit_col=bc, start_sequence=['M01'],
                       name='Mifflin Start')

    all_options = pd.read_csv(raw_data)
    fig_title = 'Implementation Sequences based on Flood Risk Elimination per Cost'
    figure = plots.implementation_sequences(all_options, [best,r_start,
                                                          w_start, m_start],
                                            title=fig_title)

    return figure
