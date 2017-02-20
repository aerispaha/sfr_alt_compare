import plotly.graph_objs as go
from pyplan import BenefitCost, plots, Sequence

plt_orange = (255, 127, 14)
plt_green =  (44, 160, 44)
plt_red = (214, 39, 40)
plt_blue = (31, 119, 180)


def nxt_phase_compare_plt(phase, nxt_phases):
    #create the Plotly chart layout object
    layout = go.Layout(
        hovermode='closest',
        plot_bgcolor='E5E5E5',
        # title='Phases From {}'.format(phase.slug),
        legend = {'x':0.05, 'y':0.9},
        xaxis = dict(title='Capital Cost (Millions)',tickprefix='$'),
        yaxis = dict(title='Parcel Hours Reduced'),
        height = 375,
    )

    phase_go = go.Scatter(
        x = phase.cost_estimate,
        y = phase.parcel_hours_reduced,
        name = str(phase.slug),
        mode = 'markers',
        marker=dict(size=10),
    )

    nx_go = [go.Scatter(
                x = [phase.cost_estimate, p.cost_estimate],
                y = [phase.parcel_hours_reduced, p.parcel_hours_reduced],
                name = str(p.slug),
                mode = 'line'
            ) for p in nxt_phases]

    #construct the Plotly figure object
    fig_data = [phase_go] + nx_go
    figure = go.Figure(data=fig_data, layout=layout)

    return figure


def next_phases_scatter(alignment, bc, next_phases, resultsfile):

    #create the Plotly chart layout object
    layout = go.Layout(
        hovermode='closest',
        plot_bgcolor='E5E5E5',
        title='Implementation Paths From {}'.format(alignment),
        legend = {'x':0.05, 'y':0.9},
        xaxis = dict(title='Capital Cost (Millions)',tickprefix='$'),
        yaxis = dict(title='Parcels with Flood Risk {}'.format(bc.benefit_col)),
        # height = '100%',
        # autosize='true',
    )


    #create the most efficient sequences from each of the next phase candidates
    sequences = [Sequence(resultsfile, benefit_col=bc.benefit_col,
                          start_sequence=[ph],
                          name='{}'.format(ph))
                 for ph in next_phases]
    #generate the other scatter graph objects with the dataframes passed in
    sequences_gos = [plots.create_scatter_trace(s.data, s.name,
                                                benefit_col = s.benefit_col)
                     for s in sequences]

    #SCATTER OF ALL OPTIONS
    all_trace = go.Scatter(
        x = [float(x) for x in bc.raw_data[bc.cost_col].tolist()],
        y = [float(y) for y in bc.raw_data[bc.benefit_col].tolist()],
        name = 'All Options',
        mode = 'markers',
        text = bc.raw_data.Option_ID.tolist(),
        visible = 'legendonly',
        marker=dict(
            opacity=0.5,
            color = 'rgb{}'.format(plt_blue)
        ),
    )

    #SINGLE POINT SHOWING CURRENT OPTION
    highlight = go.Scatter(
        x = [float(bc.raw_data.loc[bc.raw_data.Option_ID == alignment, bc.cost_col])],
        y = [float(bc.raw_data.loc[bc.raw_data.Option_ID == alignment, bc.benefit_col])],
        name = str(alignment),
        mode = 'markers',
        marker=dict(
            size=10,
        ),
    )

    #construct the Plotly figure object
    fig_data = [highlight] + sequences_gos + [all_trace]
    figure = go.Figure(data=fig_data, layout=layout)

    return figure#plots.implementation_sequences(bc.raw_data, sequences, title='cool')
    # #generate the other scatter graph objects with the dataframes passed in
    # sequences_gos = [plots.create_scatter_trace(s.data, s.name,
    #                                       benefit_col = s.benefit_col)
    #                  for s in sequences]
    #
    # #show scatter plot of cost benefit
    # all_trace = plots.create_scatter_trace(bc.raw_data,'All Projects', mode='markers',
    #                                   marker_shp='circle-open',
    #                                   benefit_col=bc.benefit_col)
    # highlight = go.Scatter(
    #     x = [float(bc.raw_data.loc[bc.raw_data.Option_ID == alignment, bc.cost_col])],
    #     y = [float(bc.raw_data.loc[bc.raw_data.Option_ID == alignment, bc.benefit_col])],
    #     name = str(alignment),
    #     mode = 'markers',
    #     marker=dict(
    #         size=10,
    #     ),
    # )
    #
    # nxtslice =bc.raw_data.loc[bc.raw_data.Option_ID.isin(next_phases)]
    # nxt_trace = plots.create_scatter_trace(nxtslice,'Next Projects', mode='markers',
    #                                   marker_shp='circle',
    #                                   benefit_col=bc.benefit_col)
    # nxtx = bc.raw_data.loc[bc.raw_data.Option_ID.isin(next_phases), bc.cost_col].tolist()
    # nxty = bc.raw_data.loc[bc.raw_data.Option_ID.isin(next_phases), bc.benefit_col].tolist()
    # nxt = go.Scatter(
    #     x = [float(x) for x in nxtx],
    #     y = [float(y) for y in nxty],
    #     name = 'Next Phase Candidates',
    #     mode = 'markers',
    #     marker=dict(
    #         size=10,
    #     ),
    # )
    # # fig = go.Figure(data=[all_trace, highlight, nxt_trace, sequences_gos])
    # return sequences_gos
