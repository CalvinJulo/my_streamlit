# -*-coding:utf-8 -*-

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


import streamlit as st
from pages.conjug import conjug
st.header(' Conjugation de Spanish')

verb = st.text('input verb')

@st.cache
def get_conjug(verb):
  verb_a_df,verb_b_df = conjug.conjug_dfs_f(verb)
  return verb_a_df,verb_b_df


verb_a_df,verb_b_df = get_conjug(verb)

mode_tense = ['Indicativo presente','Indicativo pretérito perfecto simple','Indicativo pretérito imperfecto','Indicativo futuro',
              'Condicional Condicional','Subjuntivo presente','Subjuntivo pretérito imperfecto 1','Subjuntivo futuro',
              'Imperativo Afirmativo']
mode_tense_1 = ['Indicativo presente','Indicativo pretérito perfecto compuesto','Indicativo pretérito perfecto simple',
                'Indicativo pretérito imperfecto','Indicativo pretérito pluscuamperfecto',
                'Indicativo futuro','Indicativo futuro perfecto','Condicional Condicional','Condicional perfecto',
                'Subjuntivo presente','Subjuntivo pretérito perfecto','Subjuntivo pretérito imperfecto 1',
                'Subjuntivo pretérito pluscuamperfecto 1',
                'Subjuntivo futuro','Imperativo Afirmativo','Imperativo non']

verb_a_df,verb_b_df= get_conjug(verb)

st.table(verb_a_df)
st.table(verb_b_df.loc[mode_tense])
st.table(verb_b_df.loc[mode_tense_1])

