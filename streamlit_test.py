import streamlit as st
import pandas as pd
import numpy as np
import time
import networkx as nx
import matplotlib.pyplot as plt

# see https://docs.streamlit.io/library/get-started/main-concepts

plt.rcParams["figure.figsize"] = (4, 3)

# Define function to trim edges based on weight; modified from source:
# Maksim Tsvetovat & Alexander Kouznetsov, Social Network Analysis for Startups, 2011
def trim_edges(g, weight, add_all_nodes):
    g2 = nx.Graph()
    for f, to, edata in g.edges(data=True):
        if edata['weight'] > weight or add_all_nodes == True:
            if f not in g2.nodes:
                g2.add_node(f, bipartite=g.nodes(data=True)[f]['bipartite'])
            if to not in g2.nodes:
                g2.add_node(to, bipartite=g.nodes(data=True)[to]['bipartite'])
        if edata['weight'] > weight:
            g2.add_edge(f, to, weight=edata['weight'])
    return g2

#def setFigSize(w=-1, h=-1, dpi=-1):
#    global figw
#    global figh
#    global figdpi
#    if w == -1:
#        slfigw_state = st.session_state.slfigw_key
#        w = int(slfigw_state)
#    if h == -1:
#        slfigh_state = st.session_state.slfigh_key
#        h = int(slfigh_state)
#    if dpi == -1:
#        slfigdpi_state = st.session_state.slfigdpi_key
#        dpi = int(slfigdpi_state)
#    figw = int(w)
#    figh = int(h)
#    figdpi = int(dpi)
#    drawGraph()

def drawGraph(wt=-1):
    global pos
    if wt == -1:
        sl1_state = st.session_state.sl1_key
        wt = sl1_state[0]
    gp = gp_init.copy()
    fig = plt.gcf()
    #fig = plt.figure(1, figsize=(figw, figh), dpi=figdpi)
    fig.set_size_inches(figw, figh)
    fig.set_dpi(figdpi)
    fig.clf()
    #fig.canvas.flush_events()
    plt.title('Weight>' + str(wt))

    # Trim the projected graph to the specified weight
    trimmed_gp = trim_edges(gp, wt, False)

    # Generate label dict
    labels = {}
    for node in trimmed_gp.nodes():
        labels[node] = node

    # Draw circular graph
    if pos is None:
        pos = nx.random_layout(trimmed_gp, seed=777)
    nx.draw_networkx_labels(trimmed_gp, pos=pos, labels=labels, font_size=12, font_color='black')
    nx.draw(trimmed_gp, pos=pos, **options)
    plt.margins(x=0.4)
    pp.pyplot(plt, clear_figure=True)

def animateGraph():
    nodes1 = int(sl1[0])
    nodes2 = int(sl1[1])
    step = int(sl2)
    for i in range(nodes1, nodes2, step):
        drawGraph(i)
        time.sleep(.1)
        
options = {
    'node_color': 'teal',
    'node_size': 200,
    'width': .75,
    'alpha': 0.4
}

# Set figure size
figw = 9
figh = 6
figdpi = 10
fig = plt.figure(1, figsize=(figw, figh), dpi=figdpi)
#fig = plt.figure(1)
pp = st.pyplot(fig)

sl1 = st.sidebar.slider('# of nodes', 1, 1000, (1, 1000), key='sl1_key', on_change=drawGraph)
sl2 = st.sidebar.slider('Step', 1, 100, 5)

#slfigw = st.sidebar.slider('Figure width', 1, 100, 8, key='slfigw_key', on_change=setFigSize)
#slfigh = st.sidebar.slider('Figure height', 1, 100, 8, key='slfigh_key', on_change=setFigSize)
#slfigdpi = st.sidebar.slider('Figure dpi', 1, 1000, 100, key='slfigdpi_key', on_change=setFigSize)

but1 = st.sidebar.button('Animate', on_click=animateGraph)
gp_init = nx.read_gml('gp.gml')
pos = None
drawGraph(int(sl1[0]))

st.stop()

"""
# data frame
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})
st.write(df)

# df with highlighted vals
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.dataframe(dataframe.style.highlight_max(axis=0))

# static table
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(dataframe)

# line chart
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])
st.line_chart(chart_data)

# map
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
st.map(map_data)

# slider
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

# text
st.text_input("Your name", key="name")
# You can access the value at any point with:
st.session_state.name

# checkbox
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data

# select box
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })
option = st.selectbox(
    'Which number do you like best?',
     df['first column'])
st.write('You selected: ', option)

# sidebar
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

# place widges side by side in columns
left_column, right_column = st.columns(2)
left_column.button('Press me!')
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

# progress indicator
st.write('Starting a long computation...')
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)
st.write('...and now we\'re done!')

# caching
@st.cache  # 👈 This function will be cached
def my_slow_function(arg1, arg2):
    # Do something really slow in here!
    the_output = arg1 ** arg2
    return the_output
st.write(my_slow_function(5, 20))
"""
