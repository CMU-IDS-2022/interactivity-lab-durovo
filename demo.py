import streamlit as st
import pandas as pd
import altair as alt


st.header('My first streamlit app')

st.write('Hello World')

@st.cache
def load(ur):
	return pd.read_json(ur)
df = load('https://cdn.jsdelivr.net/npm/vega-datasets@2/data/penguins.json')

if st.checkbox("Show Raw Data"):
	st.write(df)

""""
with st.echo(): <- use this for including the code as well
"""

# scatter = alt.Chart(df).mark_point().encode(
# 	alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
# 	alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
# 	alt.Color("Species")

# 	)

# st.write(scatter)

# min_weight = st.slider("Minimum Body Mass", 2500, 6500)

# st.write(min_weight)

# scatter_filtered = scatter.transform_filter(f"datum['Body Mass (g)'] >= {min_weight}")
# st.write(scatter_filtered)


# picked = alt.selection_single()
# picked = alt.selection_multi()
# picked = alt.selection_interval()
# picked = alt.selection_interval(encodings=["x"])
#picked = alt.selection_single(on='mouseover', fields=['Species', 'Island'])


# input_dropdown = alt.binding_select(options=["Adelie", "Chinstrap", "Gentoo"], name="Species of")
# picked = alt.selection_single(encodings=['color'], bind=input_dropdown)


# scatter = alt.Chart(df).mark_circle(size=100).encode(
# 	alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
# 	alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
# 	color = alt.condition(picked, "Species", alt.value('lightgray'))

# ).add_selection(picked)

# scatter = alt.Chart(df).mark_circle(size=100).encode(
# 	alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
# 	alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
# 	alt.Color("Species")

# )

# scales = alt.selection_interval(bind="scales")
# st.write(scatter.add_selection(scales))


#shortcut for panning
# scatter = alt.Chart(df).mark_circle(size=100).encode(
# 	alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
# 	alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
# 	alt.Color("Species")

# ).interactive()
# # st.write(scatter)


# hist = alt.Chart(df).mark_bar().encode(
# 	alt.X("Body Mass (g)", bin=True),
# 	alt.Y("count()"),
# 	alt.Color("Species")
# 	)

# st.write(scatter & hist)

brush = alt.selection_interval(encodings=["x"])

scatter = alt.Chart(df).mark_circle(size=100).encode(
	alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
	alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
	alt.Color("Species")

).add_selection(brush)
# st.write(scatter)


hist = alt.Chart(df).mark_bar().encode(
	alt.X("Body Mass (g)", bin=True),
	alt.Y("count()"),
	alt.Color("Species")
).transform_filter(brush)

st.write(scatter & hist)