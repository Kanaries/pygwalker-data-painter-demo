import pandas as pd
import streamlit as st
from pygwalker.api.streamlit import init_streamlit_comm, StreamlitRenderer
from pygwalker.data_parsers.database_parser import Connector

st.set_page_config(
    page_title="Streamlit Data Painter Demo",
    layout="wide"
)

st.title("Streamlit Data Painter Demo")

# Initialize pygwalker communication
init_streamlit_comm()


@st.cache_resource
def get_pyg_renderer_on_df() -> "StreamlitRenderer":
    df = pd.read_csv("./bestsellers with categories.csv")
    # When you need to publish your application, you need set `debug=False`,prevent other users to write your config file.
    return StreamlitRenderer(df, spec="ksf://bpknjjkdyyryb/demos/data_painter_demo", debug=False)


@st.cache_resource
def get_pyg_renderer_on_snowflake() -> "StreamlitRenderer":
    conn = Connector(
        st.secrets["SNOWFLAKE_URL"],
        """
            SELECT
                *
            FROM
                KANARIES.DEMO.AWS_BOOKS
        """
    )
    # When you need to publish your application, you need set `debug=False`,prevent other users to write your config file.
    return StreamlitRenderer(conn, spec="ksf://bpknjjkdyyryb/demos/data_painter_demo_snowflake", debug=False)


df_renderer = get_pyg_renderer_on_df()
snowflake_renderer = get_pyg_renderer_on_snowflake()


tab1, tab2 = st.tabs(
    ["dataframe", "snowflake"]
)

with tab1:
    df_renderer.render_explore()

with tab2:
    snowflake_renderer.render_explore()
