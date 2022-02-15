from re import U
import streamlit as st
import pandas as pd
import altair as alt

@st.cache
def load_data():
    """
    Write 1-2 lines of code here to load the data from CSV to a pandas dataframe
    and return it.
    """
    return pd.read_csv('pulse39.csv')

@st.cache
def get_slice_membership(df, genders, races, educations, age_range):
    """
    Implement a function that computes which rows of the given dataframe should
    be part of the slice, and returns a boolean pandas Series that indicates 0
    if the row is not part of the slice, and 1 if it is part of the slice.
    
    In the example provided, we assume genders is a list of selected strings
    (e.g. ['Male', 'Transgender']). We then filter the labels based on which
    rows have a value for gender that is contained in this list. You can extend
    this approach to the other variables based on how they are returned from
    their respective Streamlit components.
    """
    labels = pd.Series([1] * len(df), index=df.index)
    if genders:
        labels &= df['gender'].isin(genders)
    if races:
        labels &= df['race'].isin(races)
    if educations:
        labels &= df['education'].isin(educations)
    if age_range:
        # df['age_group'] = df['age_group'].astype(int)
        labels &= (df['age'] <= age_range[1]) & (df['age'] >= age_range[0])
        # labels &= df.age_group.isin(age_range)
    # ... complete this function for the other demographic variables
    return labels

def make_long_reason_dataframe(df, reason_prefix):
    """
    ======== You don't need to edit this =========
    
    Utility function that converts a dataframe containing multiple columns to
    a long-style dataframe that can be plotted using Altair. For example, say
    the input is something like:
    
         | why_no_vaccine_Reason 1 | why_no_vaccine_Reason 2 | ...
    -----+-------------------------+-------------------------+------
    1    | 0                       | 1                       | 
    2    | 1                       | 1                       |
    
    This function, if called with the reason_prefix 'why_no_vaccine_', will
    return a long dataframe:
    
         | id | reason      | agree
    -----+----+-------------+---------
    1    | 1  | Reason 2    | 1
    2    | 2  | Reason 1    | 1
    3    | 2  | Reason 2    | 1
    
    For every person (in the returned id column), there may be one or more
    rows for each reason listed. The agree column will always contain 1s, so you
    can easily sum that column for visualization.
    """
    reasons = df[[c for c in df.columns if c.startswith(reason_prefix)]].copy()
    reasons['id'] = reasons.index
    reasons = pd.wide_to_long(reasons, reason_prefix, i='id', j='reason', suffix='.+')
    reasons = reasons[~pd.isna(reasons[reason_prefix])].reset_index().rename({reason_prefix: 'agree'}, axis=1)
    return reasons


# MAIN CODE


st.title("Household Pulse Explorable")
with st.spinner(text="Loading data..."):
    df = load_data()
st.text("Visualize the overall dataset and some distributions here...")
st.write(df)

education_bar = alt.Chart(df).mark_bar().encode(
    alt.X('education'),
    alt.Y('count(received_vaccine)'),
    color=alt.Color('received_vaccine'),
    tooltip=['race']
    ).interactive()
st.write(education_bar)

education_bar = alt.Chart(df).mark_bar().encode(
    alt.X('race'),
    alt.Y("count(received_vaccine)"),
    color=alt.Color('received_vaccine')
    ).interactive()
st.write(education_bar)


race_education = alt.Chart(df).mark_bar().encode(
    alt.X('race'),
    alt.Y("education"),
    color=alt.Color('count()')
    ).interactive()
st.write(race_education)

st.header("Custom slicing")


df_long = make_long_reason_dataframe(df, 'why_no_vaccine_')
df_long = df.join(df_long)
st.write(df_long.head())
# df_long = df

races = st.multiselect('Select Races', df_long['race'].unique().tolist())

genders = st.multiselect('Select Gender', df_long.gender.unique())

educations = st.multiselect('Select Education Level', df_long.education.unique())

# age_range = st.slider('Select Age Range', df_long.age.min(), df_long.age.max())
age_range = st.slider('Select Age Range', int(df_long.age.min()), int(df_long.age.max()), (0, 100))
st.write(age_range)

filtered_data = df_long.loc[get_slice_membership(df_long, genders, races, educations, age_range)]

# st.write(filtered_data)
# sliced_chart = alt.Chart(filtered_data).mark_bar().encode(
#     alt.X('reason'),
#     alt.Y('count(vaccine_intention)')
# )
chart = alt.Chart(filtered_data, title='In Slice').mark_bar().encode(
    x='sum(agree)',
    y='reason:O',
).interactive()

st.write(chart)



st.header("Person sampling")
st.text("Implement a button to sample and describe a random person here...")
