import streamlit as st
import pandas as pd
import plotly.express as px
from modules.data_loader import load_investigations
from modules.relevance_engine import rank_investigations
from modules.gap_detector import detect_gaps

st.set_page_config(page_title="FLARE | Space Fire Safety Intelligence", page_icon="🔥", layout="wide")
st.markdown("""
<style>
.block-container {padding-top: 1.5rem; max-width: 1500px;}
.hero {padding: 1.4rem 1.6rem; border-radius: 18px; background: linear-gradient(120deg,#101b35,#203b5d); color:white; margin-bottom:1rem;}
.hero h1 {font-size:2.7rem; margin:0;}
.hero p {color:#d8e5f5; margin:.3rem 0 0 0;}
.small-note {color:#718096; font-size:.85rem;}
</style>
""", unsafe_allow_html=True)

df=load_investigations()
records=df.to_dict("records")

st.markdown('<div class="hero"><h1>🔥 FLARE</h1><p>Fire Learning, Analysis & Risk Exploration · NASA microgravity combustion intelligence</p></div>', unsafe_allow_html=True)
st.warning("Research prototype: starter records contain unverified or incomplete metadata. Scores are relevance heuristics, not fire-risk probabilities or certified safety assessments.")

with st.sidebar:
    st.header("Habitat scenario")
    scenario=st.selectbox("Select environment",["Lunar habitat","ISS reference","Spacesuit","Custom"])
    presets={
        "Lunar habitat":{"o2":30.0,"pressure":10.2},
        "ISS reference":{"o2":21.0,"pressure":14.7},
        "Spacesuit":{"o2":100.0,"pressure":4.3},
        "Custom":{"o2":30.0,"pressure":10.2}
    }
    p=presets[scenario]
    oxygen=st.slider("Target oxygen concentration (%)",1.0,100.0,float(p["o2"]),0.5)
    pressure=st.slider("Target pressure (psi)",1.0,20.0,float(p["pressure"]),0.1)
    airflow=st.number_input("Target airflow (m/s)",min_value=0.0,max_value=10.0,value=0.5,step=0.1)
    materials=st.multiselect("Relevant fuel/material categories",["solid","liquid","gas","mixed"],default=["solid","mixed"])
    pillars=st.multiselect("Fire-safety priorities",["prevention","detection","suppression"],default=["prevention","detection","suppression"])
    st.caption("Atmospheric targets are scenario assumptions. Edit them for your mission concept.")

target={"oxygen_pct":oxygen,"pressure_psi":pressure,"airflow_m_s":airflow,"material_categories":materials,"safety_pillars":pillars}
ranked=rank_investigations(records,target)
valid=[r for r in ranked if r["score"] is not None]
c1,c2,c3,c4=st.columns(4)
c1.metric("Investigations indexed",len(records))
c2.metric("With rankable metadata",len(valid))
c3.metric("Target oxygen",f"{oxygen:.1f}%")
c4.metric("Target pressure",f"{pressure:.1f} psi")

tab1,tab2,tab3,tab4,tab5=st.tabs(["Habitat Explorer","Atmosphere Atlas","Compare Studies","Research Gaps","Data Catalogue"])
with tab1:
    st.subheader(f"Research relevance for {scenario}")
    st.caption("Ranking uses available metadata only. Coverage indicates how much of the scoring model could be evaluated.")
    if valid:
        for r in valid[:8]:
            with st.container(border=True):
                left,right=st.columns([4,1])
                left.markdown(f"**{r['name']}** · `{r['id']}`")
                left.write(r.get("description",""))
                left.caption("Pillars: "+", ".join(r.get("safety_pillars",[]))+" · Hardware: "+str(r.get("hardware") or "Not reported"))
                right.metric("Relevance",f"{r['score']:.1f}/100")
                right.caption(f"Metadata coverage: {r['coverage']:.0f}%")
                right.caption(f"Confidence: {r['confidence']}")
                with st.expander("Why this score?"):
                    st.json(r["components"])
                    st.write("This is a research-discovery ranking, not a prediction of ignition likelihood or fire severity.")
    else:
        st.info("Not enough verified metadata to calculate a meaningful ranking. Add numeric experiment conditions to the dataset.")
with tab2:
    st.subheader("Experimental atmosphere coverage")
    plot_df=df.dropna(subset=["oxygen_pct","pressure_psi"])
    if plot_df.empty:
        st.info("No verified oxygen/pressure pairs are loaded yet. The starter records intentionally leave unavailable numeric values blank rather than inventing experimental conditions.")
        st.markdown("**Next data task:** extract run-level oxygen concentration and pressure from PSI records and source publications.")
    else:
        fig=px.scatter(plot_df,x="oxygen_pct",y="pressure_psi",color="fuel_category",hover_name="name",hover_data=["project","gravity_regime"])
        fig.add_vrect(x0=max(0,oxygen-5),x1=min(100,oxygen+5),fillcolor="orange",opacity=.12,line_width=0,annotation_text="Target O₂ band")
        fig.add_hrect(y0=max(0,pressure-1),y1=pressure+1,fillcolor="orange",opacity=.08,line_width=0)
        st.plotly_chart(fig,use_container_width=True)
    st.caption("A blank plot is an honest representation of missing structured data, not a system failure.")
with tab3:
    st.subheader("Side-by-side investigation comparison")
    names=st.multiselect("Choose investigations",df["name"].tolist(),default=df["name"].head(3).tolist(),max_selections=4)
    comp=df[df["name"].isin(names)].set_index("name")
    if not comp.empty:
        fields=["project","description","fuel_category","fuel_materials","oxygen_pct","pressure_psi","airflow_m_s","gravity_regime","hardware","sensors","measurements","safety_pillars","data_status","source_url"]
        st.dataframe(comp[fields].T, use_container_width=True)
with tab4:
    st.subheader("Scientific and metadata gaps")
    for gap in detect_gaps(records):
        with st.container(border=True):
            st.markdown(f"**{gap['title']}**")
            st.caption(f"Priority: {gap['severity']}")
            st.write(gap["detail"])
            st.info(gap["recommendation"])
    st.caption("Gap findings apply to the currently loaded starter dataset. Expand and verify the corpus before making repository-wide claims.")
with tab5:
    st.subheader("Investigation catalogue")
    view=df[["id","name","project","fuel_category","gravity_regime","safety_pillars","data_status","source_url"]].copy()
    st.dataframe(view,use_container_width=True,hide_index=True)
    st.download_button("Download current catalogue (CSV)",view.to_csv(index=False).encode("utf-8"),"flare_catalogue.csv","text/csv")
    st.download_button("Download raw records (JSON)",open("data/investigations.json","rb").read(),"flare_investigations.json","application/json")

st.divider()
st.markdown("**FLARE research prototype** · Built for NASA Space Apps Challenge 2026 · Open research, transparent assumptions, traceable evidence.")
