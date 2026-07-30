import streamlit as st
from datetime import datetime

# Screen Fabricator V05
# Created by Bryce P Mulligan, PhD, CPsych
#
# CHANGE LOG V05
# - Expanded Home page with orientation and documentation
# - Mental-health-focused positioning
# - Added critical item support for Total Score Entry tools
# - Removed manual safety-trigger checkbox
# - Moved Recommended Actions below Scoring Simulator
# - Replaced numeric sliders with number_input fields
# - Larger Immediate Safety Concern alert
# - Improved Manage Tools display

st.set_page_config(page_title='Screen Fabricator V05', layout='wide')

st.title('🧩 Screen Fabricator V05')
st.caption('Created by Bryce P Mulligan, PhD, CPsych')
st.markdown('*Build custom mental health screening, scoring, triage, and safety-alert workflows.*')

if 'screening_tools' not in st.session_state:
    st.session_state.screening_tools = {}

page = st.sidebar.radio(
    'Navigation',
    ['🏠 Home', '🛠️ Build Screening Tool', '📋 Use a Tool', '💾 Manage Tools']
)

if page == '🏠 Home':
    st.header('Welcome')
    st.markdown('''
    Screen Fabricator is a prototype application designed to help clinicians create,
    test, and administer custom mental health screening and triage workflows.
    ''')

    st.subheader('Intended Use')
    st.markdown('''
    - Depression screening
    - Anxiety screening
    - Suicide-risk and safety screening
    - Mental health intake workflows
    - Mental health triage and referral pathways
    - Educational and research demonstrations
    ''')

    st.subheader('General Workflow')
    st.markdown('''
    1. Build a screening tool
    2. Define scoring thresholds
    3. Test scoring using the simulator
    4. Add recommended actions
    5. Save the tool
    6. Use or share the tool
    ''')

    st.subheader('Important Limitations')
    st.warning(
        'Tools created using Screen Fabricator are user-generated and are not automatically validated. '
        'Responsibility for validation, interpretation, and implementation remains with the tool creator.'
    )

    st.subheader('Version Information')
    st.info('Screen Fabricator V05\n\nCreated by Bryce P Mulligan, PhD, CPsych')

    st.subheader('Coming Soon')
    st.markdown('- Import / Export tools\n- Example tool library\n- Tool duplication\n- Enhanced sharing features')

elif page == '🛠️ Build Screening Tool':
    tool_name = st.text_input('Tool Name')
    focus = st.text_input('Focus Area')
    desc = st.text_area('Description')
    instructions = st.text_area('Instructions for Respondents')

    method = st.radio('Scoring Method', ['Questionnaire-Based Scoring', 'Total Score Entry'])

    questions = []
    critical_items = []

    if method == 'Questionnaire-Based Scoring':
        n = st.number_input('Number of Questions', min_value=1, value=5)

        for i in range(int(n)):
            st.subheader(f'Question {i+1}')
            qt = st.text_input('Question Text', key=f'q{i}')
            qtype = st.selectbox('Type', ['Multiple Choice', 'Yes/No', 'Numeric Scale'], key=f't{i}')
            q = {'text': qt, 'type': qtype}

            if qtype == 'Multiple Choice':
                raw = st.text_input('Options (comma separated)', key=f'o{i}')
                opts = [x.strip() for x in raw.split(',') if x.strip()]
                scores = {}
                for opt in opts:
                    scores[opt] = st.number_input(f'Score: {opt}', value=0, key=f's{i}{opt}')
                q['options'] = opts
                q['scores'] = scores

                if st.checkbox('Safety Indicator', key=f'c{i}'):
                    q['safety_indicator'] = True
                    q['trigger_responses'] = st.multiselect('Trigger Responses', opts, key=f'tr{i}')

            elif qtype == 'Yes/No':
                q['scores'] = {'Yes': 1, 'No': 0}
                q['safety_indicator'] = st.checkbox('Safety Indicator', key=f'yn{i}')

            else:
                mn = st.number_input('Minimum', value=0, key=f'mn{i}')
                mx = st.number_input('Maximum', value=10, key=f'mx{i}')
                q['min_value'] = mn
                q['max_value'] = mx

                if st.checkbox('Safety Indicator', key=f'ns{i}'):
                    q['safety_indicator'] = True
                    q['trigger_value'] = st.number_input('Trigger if >=', value=int(mx), key=f'tv{i}')

            questions.append(q)

    else:
        st.subheader('Total Score Configuration')
        st.number_input('Maximum Possible Score', value=27)

        st.subheader('Critical Item Definitions')
        critical_count = st.number_input('Number of Critical Items', min_value=0, value=1)

        for i in range(int(critical_count)):
            label = st.text_input(f'Critical Item {i+1} Label', key=f'crit_label_{i}')
            threshold = st.number_input(f'Critical Item {i+1} Trigger Threshold', min_value=0, value=1, key=f'crit_thr_{i}')
            critical_items.append({'label': label, 'threshold': threshold})

    st.subheader('Symptom Elevation Thresholds')
    low_max = st.number_input('Low Upper Bound', value=4)
    mod_max = st.number_input('Moderate Upper Bound', value=14)

    low_desc = st.text_area('Low Description', value='Low symptom elevation')
    mod_desc = st.text_area('Moderate Description', value='Moderate symptom elevation')
    high_desc = st.text_area('High Description', value='High symptom elevation')

    purple_desc = st.text_area('Purple Alert Description', value='Immediate safety concern identified')

    st.subheader('Scoring Simulator')
    sim = st.number_input('Sample Score', value=0)

    if st.button('Test Scoring'):
        if sim <= low_max:
            st.success('🟢 Low Symptom Elevation')
        elif sim <= mod_max:
            st.warning('🟡 Moderate Symptom Elevation')
        else:
            st.error('🔴 High Symptom Elevation')

    st.subheader('Recommended Actions')
    low_act = st.text_area('Low Recommended Actions', value='Monitor as appropriate')
    mod_act = st.text_area('Moderate Recommended Actions', value='Further assessment recommended')
    high_act = st.text_area('High Recommended Actions', value='Prompt intervention recommended')
    purple_act = st.text_area('Purple Alert Actions', value='Conduct immediate safety assessment')

    if st.button('Save Tool') and tool_name:
        st.session_state.screening_tools[tool_name] = {
            'name': tool_name,
            'focus': focus,
            'description': desc,
            'instructions': instructions,
            'method': method,
            'questions': questions,
            'critical_items': critical_items,
            'low_max': low_max,
            'mod_max': mod_max,
            'levels': {
                'low': {'description': low_desc, 'actions': low_act},
                'moderate': {'description': mod_desc, 'actions': mod_act},
                'high': {'description': high_desc, 'actions': high_act},
                'purple': {'description': purple_desc, 'actions': purple_act}
            },
            'created': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        st.success('Tool saved.')

elif page == '📋 Use a Tool':
    if st.session_state.screening_tools:
        name = st.selectbox('Select Tool', list(st.session_state.screening_tools.keys()))
        tool = st.session_state.screening_tools[name]

        st.info(tool.get('instructions', ''))

        total = 0
        purple = False

        if tool['method'] == 'Questionnaire-Based Scoring':
            for i, q in enumerate(tool['questions']):
                if q['type'] == 'Multiple Choice':
                    r = st.radio(q['text'], q.get('options', []), key=f'r{i}')
                    total += q.get('scores', {}).get(r, 0)
                    if q.get('safety_indicator') and r in q.get('trigger_responses', []):
                        purple = True

                elif q['type'] == 'Yes/No':
                    r = st.radio(q['text'], ['Yes', 'No'], key=f'ynr{i}')
                    total += 1 if r == 'Yes' else 0
                    if q.get('safety_indicator') and r == 'Yes':
                        purple = True

                else:
                    r = st.number_input(
                        q['text'],
                        min_value=int(q['min_value']),
                        max_value=int(q['max_value']),
                        step=1,
                        key=f'num_{i}'
                    )
                    total += r
                    if q.get('safety_indicator') and r >= q.get('trigger_value', 999):
                        purple = True
        else:
            total = st.number_input('Total Score', value=0)
            for i, item in enumerate(tool.get('critical_items', [])):
                score = st.number_input(item['label'], value=0, key=f'critical_{i}')
                if score >= item['threshold']:
                    purple = True

        if st.button('Calculate Result'):
            if total <= tool['low_max']:
                level = 'low'; icon = '🟢'
            elif total <= tool['mod_max']:
                level = 'moderate'; icon = '🟡'
            else:
                level = 'high'; icon = '🔴'

            st.markdown(f'## {icon} {level.title()} Symptom Elevation')
            st.write(tool['levels'][level]['description'])
            st.write(tool['levels'][level]['actions'])

            if purple:
                st.markdown(
                    """
                    <div style='background:#7D3C98;padding:20px;border-radius:12px;text-align:center;margin-top:20px;'>
                    <h1 style='color:white;'>🟣 IMMEDIATE SAFETY CONCERN</h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.write(tool['levels']['purple']['description'])
                st.write(tool['levels']['purple']['actions'])
            else:
                st.success('No Immediate Safety Concern Identified')

else:
    st.header('Manage Tools')
    for name in list(st.session_state.screening_tools.keys()):
        with st.expander(name):
            st.json(st.session_state.screening_tools[name])
