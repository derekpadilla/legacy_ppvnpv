import dash
from dash import dcc, html, dash_table, Input, Output
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots



server = app.server

# Custom CSS styles
external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title='PredictiveValue.info')

# Define color scheme
colors = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#43AA8B',
    'background': '#F8F9FA',
    'card': '#FFFFFF',
    'text': '#2C3E50',
    'text_light': '#6C757D'
}

app.layout = html.Div([
    # Header Section
    html.Div([
        html.Div([
            html.H1([
                html.I(className="fas fa-calculator", style={'marginRight': '15px', 'color': colors['accent']}),
                "Predictive Value Calculator"
            ], style={
                'color': 'white',
                'fontSize': '2.5rem',
                'fontWeight': 'bold',
                'margin': '0',
                'textAlign': 'center'
            }),
            html.P("Interactive tool for calculating positive and negative predictive values",
                   style={
                       'color': 'rgba(255,255,255,0.9)',
                       'fontSize': '1.1rem',
                       'textAlign': 'center',
                       'margin': '10px 0 0 0'
                   })
        ], style={'padding': '40px 20px'})
    ], style={
        'background': f'linear-gradient(135deg, {colors["primary"]}, {colors["secondary"]})',
        'marginBottom': '30px'
    }),

    # Main Content Container
    html.Div([
        # Input Parameters Card
        html.Div([
            html.Div([
                html.H3([
                    html.I(className="fas fa-sliders-h", style={'marginRight': '10px', 'color': colors['primary']}),
                    "Test Parameters"
                ], style={'color': colors['text'], 'marginBottom': '20px'}),

                html.P("Enter the sensitivity and specificity values for your diagnostic test. These values are typically provided by the test manufacturer or regulatory bodies like the FDA.",
                       style={'color': colors['text_light'], 'marginBottom': '25px', 'lineHeight': '1.6'}),

                # Input controls with better styling
                html.Div([
                    html.Div([
                        html.Label([
                            html.I(className="fas fa-search-plus", style={'marginRight': '8px', 'color': colors['success']}),
                            "Sensitivity (%)"
                        ], style={'fontWeight': 'bold', 'color': colors['text'], 'marginBottom': '8px', 'display': 'block'}),
                        dcc.Input(
                            id='sens',
                            value=98,
                            type='number',
                            min=0,
                            max=100,
                            step=0.1,
                            style={
                                'width': '100%',
                                'padding': '12px',
                                'border': f'2px solid {colors["primary"]}',
                                'borderRadius': '8px',
                                'fontSize': '16px',
                                'outline': 'none'
                            }
                        ),
                        html.Small("Percentage of true positives correctly identified",
                                 style={'color': colors['text_light'], 'fontStyle': 'italic'})
                    ], style={'marginBottom': '20px'}),

                    html.Div([
                        html.Label([
                            html.I(className="fas fa-search-minus", style={'marginRight': '8px', 'color': colors['accent']}),
                            "Specificity (%)"
                        ], style={'fontWeight': 'bold', 'color': colors['text'], 'marginBottom': '8px', 'display': 'block'}),
                        dcc.Input(
                            id='spec',
                            value=85,
                            type='number',
                            min=0,
                            max=100,
                            step=0.1,
                            style={
                                'width': '100%',
                                'padding': '12px',
                                'border': f'2px solid {colors["secondary"]}',
                                'borderRadius': '8px',
                                'fontSize': '16px',
                                'outline': 'none'
                            }
                        ),
                        html.Small("Percentage of true negatives correctly identified",
                                 style={'color': colors['text_light'], 'fontStyle': 'italic'})
                    ])
                ])
            ], style={
                'padding': '30px',
                'backgroundColor': colors['card'],
                'borderRadius': '12px',
                'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
                'border': '1px solid #E9ECEF'
            })
        ], style={'marginBottom': '30px'}),

        # Results Summary Card
        html.Div(id='results-summary', style={'marginBottom': '30px'}),

        # Graph Card
        html.Div([
            html.Div([
                html.H3([
                    html.I(className="fas fa-chart-line", style={'marginRight': '10px', 'color': colors['primary']}),
                    "Predictive Values vs. Prevalence"
                ], style={'color': colors['text'], 'marginBottom': '15px'}),

                html.P("The graph below shows how positive and negative predictive values change with disease prevalence in the population.",
                       style={'color': colors['text_light'], 'marginBottom': '20px', 'lineHeight': '1.6'}),

                html.Div(id='output-graph')
            ], style={
                'padding': '30px',
                'backgroundColor': colors['card'],
                'borderRadius': '12px',
                'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
                'border': '1px solid #E9ECEF'
            })
        ], style={'marginBottom': '30px'}),

        # Information Cards
        html.Div([
            # Definitions Card
            html.Div([
                html.H4([
                    html.I(className="fas fa-book", style={'marginRight': '10px', 'color': colors['primary']}),
                    "Definitions"
                ], style={'color': colors['text'], 'marginBottom': '20px'}),

                html.Div([
                    html.Div([
                        html.H5([
                            html.I(className="fas fa-plus-circle", style={'marginRight': '8px', 'color': colors['success']}),
                            "Positive Predictive Value (PPV)"
                        ], style={'color': colors['success'], 'marginBottom': '10px'}),
                        html.P("Percentage of positive test results that are true positives (correct).",
                               style={'color': colors['text'], 'marginBottom': '10px'}),
                        html.Code("PPV = (Sensitivity × Prevalence) / [(Sensitivity × Prevalence) + (100 - Specificity) × (100 - Prevalence)]",
                                style={'backgroundColor': '#F8F9FA', 'padding': '8px', 'borderRadius': '4px', 'display': 'block', 'fontSize': '12px'})
                    ], style={'marginBottom': '25px'}),

                    html.Div([
                        html.H5([
                            html.I(className="fas fa-minus-circle", style={'marginRight': '8px', 'color': colors['accent']}),
                            "Negative Predictive Value (NPV)"
                        ], style={'color': colors['accent'], 'marginBottom': '10px'}),
                        html.P("Percentage of negative test results that are true negatives (correct).",
                               style={'color': colors['text'], 'marginBottom': '10px'}),
                        html.Code("NPV = [Specificity × (100 - Prevalence)] / [(100 - Sensitivity) × Prevalence + Specificity × (100 - Prevalence)]",
                                style={'backgroundColor': '#F8F9FA', 'padding': '8px', 'borderRadius': '4px', 'display': 'block', 'fontSize': '12px'})
                    ], style={'marginBottom': '25px'}),

                    html.Div([
                        html.H5([
                            html.I(className="fas fa-percentage", style={'marginRight': '8px', 'color': colors['secondary']}),
                            "Prevalence"
                        ], style={'color': colors['secondary'], 'marginBottom': '10px'}),
                        html.P("The percentage of the population that actually has the condition being tested for.",
                               style={'color': colors['text']})
                    ])
                ])
            ], style={
                'padding': '25px',
                'backgroundColor': colors['card'],
                'borderRadius': '12px',
                'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
                'border': '1px solid #E9ECEF',
                'marginBottom': '20px'
            }),

            # Example Card
            html.Div([
                html.H4([
                    html.I(className="fas fa-lightbulb", style={'marginRight': '10px', 'color': colors['accent']}),
                    "Clinical Example"
                ], style={'color': colors['text'], 'marginBottom': '20px'}),

                html.Div([
                    html.P("Consider a diagnostic test with:", style={'fontWeight': 'bold', 'color': colors['text'], 'marginBottom': '10px'}),
                    html.Ul([
                        html.Li("90% sensitivity", style={'color': colors['text'], 'marginBottom': '5px'}),
                        html.Li("85% specificity", style={'color': colors['text'], 'marginBottom': '5px'}),
                        html.Li("5% disease prevalence in the population", style={'color': colors['text'], 'marginBottom': '15px'})
                    ]),
                    html.P("Results:", style={'fontWeight': 'bold', 'color': colors['text'], 'marginBottom': '10px'}),
                    html.Ul([
                        html.Li([html.Strong("PPV: 24%"), " - Only 24% of positive test results would be correct"],
                               style={'color': colors['text'], 'marginBottom': '5px'}),
                        html.Li([html.Strong("NPV: 99%"), " - 99% of negative test results would be correct"],
                               style={'color': colors['text']})
                    ])
                ], style={'backgroundColor': '#F8F9FA', 'padding': '20px', 'borderRadius': '8px', 'borderLeft': f'4px solid {colors["accent"]}'})
            ], style={
                'padding': '25px',
                'backgroundColor': colors['card'],
                'borderRadius': '12px',
                'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
                'border': '1px solid #E9ECEF'
            })
        ])

    ], style={
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '0 20px'
    }),

    # Footer
    html.Div([
        html.P([
            "Created by ",
            html.A("Derek Padilla", href="https://derekpadilla.com", target="_blank",
                   style={'color': colors['primary'], 'textDecoration': 'none'}),
            " using Plotly's ",
            html.A("Dash", href="https://plotly.com/dash/", target="_blank",
                   style={'color': colors['primary'], 'textDecoration': 'none'}),
            " Python framework. Enhanced with modern UI design."
        ], style={
            'textAlign': 'center',
            'color': colors['text_light'],
            'fontSize': '14px',
            'padding': '30px 20px'
        })
    ])

], style={
    'backgroundColor': colors['background'],
    'minHeight': '100vh',
    'fontFamily': 'Arial, sans-serif'
})

@app.callback(
    [Output('output-graph', 'children'),
     Output('results-summary', 'children')],
    [Input('sens', 'value'),
     Input('spec', 'value')]
)
def update_outputs(sens, spec):
    if sens is None or spec is None:
        return html.Div(), html.Div()

    # Calculate predictive values across prevalence range
    prev = np.linspace(0.1, 99.9, 1000)  # Avoid division by zero
    ppv = 100 * (sens * prev) / ((sens * prev) + ((100 - spec) * (100 - prev)))
    npv = 100 * (spec * (100 - prev)) / (((100 - sens) * prev) + ((spec * (100 - prev))))

    # Create enhanced graph
    fig = go.Figure()

    # Add PPV line
    fig.add_trace(go.Scatter(
        x=prev,
        y=ppv,
        mode='lines',
        name='Positive Predictive Value (PPV)',
        line=dict(color=colors['success'], width=4),
        hovertemplate='<b>PPV</b><br>Prevalence: %{x:.1f}%<br>PPV: %{y:.1f}%<extra></extra>'
    ))

    # Add NPV line
    fig.add_trace(go.Scatter(
        x=prev,
        y=npv,
        mode='lines',
        name='Negative Predictive Value (NPV)',
        line=dict(color=colors['accent'], width=4),
        hovertemplate='<b>NPV</b><br>Prevalence: %{x:.1f}%<br>NPV: %{y:.1f}%<extra></extra>'
    ))

    # Update layout
    fig.update_layout(
        xaxis_title="Disease Prevalence (%)",
        yaxis_title="Predictive Value (%)",
        hovermode='x unified',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        margin=dict(t=50, b=50, l=50, r=50),
        height=500
    )

    # Add grid
    fig.update_xaxis(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxis(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')

    graph = dcc.Graph(
        id='graph',
        figure=fig,
        config={'displayModeBar': True, 'displaylogo': False}
    )

    # Calculate specific examples for common prevalence values
    common_prev = [1, 5, 10, 20, 50]
    results_data = []

    for p in common_prev:
        ppv_val = 100 * (sens * p) / ((sens * p) + ((100 - spec) * (100 - p)))
        npv_val = 100 * (spec * (100 - p)) / (((100 - sens) * p) + ((spec * (100 - p))))
        results_data.append({
            'Prevalence (%)': f"{p}%",
            'PPV (%)': f"{ppv_val:.1f}%",
            'NPV (%)': f"{npv_val:.1f}%"
        })

    # Create results summary
    results_summary = html.Div([
        html.Div([
            html.H3([
                html.I(className="fas fa-table", style={'marginRight': '10px', 'color': colors['primary']}),
                "Quick Reference Table"
            ], style={'color': colors['text'], 'marginBottom': '15px'}),

            html.P(f"Based on Sensitivity: {sens}% and Specificity: {spec}%",
                   style={'color': colors['text_light'], 'marginBottom': '20px'}),

            dash_table.DataTable(
                data=results_data,
                columns=[
                    {"name": "Prevalence", "id": "Prevalence (%)"},
                    {"name": "PPV", "id": "PPV (%)"},
                    {"name": "NPV", "id": "NPV (%)"}
                ],
                style_cell={
                    'textAlign': 'center',
                    'padding': '12px',
                    'fontFamily': 'Arial, sans-serif',
                    'fontSize': '14px'
                },
                style_header={
                    'backgroundColor': colors['primary'],
                    'color': 'white',
                    'fontWeight': 'bold'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#F8F9FA'
                    }
                ]
            )
        ], style={
            'padding': '30px',
            'backgroundColor': colors['card'],
            'borderRadius': '12px',
            'boxShadow': '0 4px 15px rgba(0,0,0,0.1)',
            'border': '1px solid #E9ECEF'
        })
    ])

    return graph, results_summary

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_ui=False, dev_tools_props_check=False, host='0.0.0.0')