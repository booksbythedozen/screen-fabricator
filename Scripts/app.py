import json
import streamlit as st
from datetime import datetime

st.set_page_config(page_title='Screen Fabricator V07', layout='wide')

st.title('🧩 Screen Fabricator V07')
st.caption(
    'Created by Bryce P Mulligan, PhD, CPsych | '
    'Version 07 Pilot Release | '
    '30 July 2026'
)
st.markdown('*Fast Tool Creation. Clear Clinical Guidance.*')

if 'screening_tools' not in st.session_state:
    st.session_state.screening_tools = {}


def get_level(score, low_max, mod_max):
    if score <= low_max:
        return 'low', '✅', 'Low Symptom Elevation'
    elif score <= mod_max:
        return 'moderate', '⚠️', 'Moderate Symptom Elevation'
    return 'high', '❗', 'Severe Symptom Elevation'


page = st.sidebar.radio(
    'Navigation',
    ['🏠 Home', '🛠️ Build Screening Tool', '📋 Use a Tool', '💾 Manage Tools']
)

if page == '🏠 Home':

    st.header('Welcome to Screen Fabricator')

    st.markdown("""
    Screen Fabricator is a prototype application designed to help clinicians create,
    test, and administer custom mental health screening and triage workflows.

    Intended uses include:

    - Depression screening
    - Anxiety screening
    - Suicide-risk and safety screening
    - Mental health intake workflows
    - Mental health triage and referral pathways
    - Educational and research demonstrations

    ### Typical Workflow

    1. Build a screening tool
    2. Define scoring thresholds
    3. Configure recommendations
    4. Test the tool
    5. Deploy for clinical or organizational use

    ### Pilot Testing Feedback

    After testing a tool, users may wish to document:

    - Anything confusing
    - Anything unnecessarily complicated
    - Missing functionality
    - Suggestions for improvement

    Early feedback is strongly encouraged.
    """)

    st.subheader('Who Is This For?')
    st.markdown("""
    - Psychologists
    - Mental health clinicians
    - Program managers
    - Researchers
    - Quality improvement teams
    - Healthcare administrators
    """)

    st.subheader('What Can Be Built?')
    st.markdown("""
    - Depression screeners
    - Anxiety screeners
    - Suicide risk triage tools
    - Intake workflows
    - Research eligibility screeners
    - Service navigation tools
    """)

elif page == '🛠️ Build Screening Tool':

    st.markdown('**Tool Name**')
    st.markdown('*Enter a clear name that will appear in the tool selection list.*')
    tool_name = st.text_input('Tool Name', label_visibility='collapsed')

    st.markdown('**Focus Area**')
    st.markdown('*Specify the clinical, research, or program area addressed by this tool.*')
    focus = st.text_input('Focus Area', label_visibility='collapsed')

    st.markdown('**Description**')
    st.markdown('*Provide a brief overview of the tool purpose and intended use.*')
    description = st.text_area('Description', label_visibility='collapsed')

    st.markdown('**Instructions for Respondents**')
    st.markdown('*These instructions will be shown to respondents before they begin.*')
    instructions = st.text_area('Instructions for Respondents', label_visibility='collapsed')

    method = st.radio(
        'Scoring Method',
        ['Questionnaire-Based Scoring', 'Total Score Entry']
    )

    questions = []
    critical_items = []
    shared_template = None

    if method == 'Questionnaire-Based Scoring':

        response_mode = st.radio(
            'Response Structure',
            ['Use same response options for all items', 'Custom response options per item']
        )

        if response_mode == 'Use same response options for all items':
            st.subheader('Shared Response Template')
            raw = st.text_input(
                'Options (comma separated)',
                value='Not at all, Several days, More than half the days, Nearly every day'
            )
            opts = [x.strip() for x in raw.split(',') if x.strip()]
            scores = {}

            for opt in opts:
                scores[opt] = st.number_input(
                    f'Score for {opt}',
                    value=max(0, opts.index(opt)),
                    key=f'temp_{opt}'
                )

            shared_template = {'options': opts, 'scores': scores}

        n = st.number_input('Number of Questions', min_value=1, value=9)

        for i in range(int(n)):
            st.subheader(f'Question {i + 1}')
            qt = st.text_input('Question Text', key=f'q{i}')

            q = {'text': qt, 'type': 'Multiple Choice'}

            if shared_template:
                q['options'] = shared_template['options']
                q['scores'] = shared_template['scores']
            else:
                raw = st.text_input('Options (comma separated)', key=f'opt_{i}')
                opts = [x.strip() for x in raw.split(',') if x.strip()]
                scores = {}
                for opt in opts:
                    scores[opt] = st.number_input(
                        f'Score: {opt}',
                        value=0,
                        key=f's_{i}_{opt}'
                    )
                q['options'] = opts
                q['scores'] = scores

            q['reverse_scored'] = st.checkbox('Reverse Scored', key=f'rev_{i}')

            q['safety_indicator'] = st.checkbox(
                'Safety Indicator',
                help='Enable this when certain responses indicate immediate risk and should trigger a Safety Alert regardless of total score.',
                key=f'safe_{i}'
            )

            if q['safety_indicator']:
                q['trigger_responses'] = st.multiselect(
                    'Trigger Responses',
                    q['options'],
                    help='Responses indicating an immediate safety concern.',
                    key=f'trig_{i}'
                )

            questions.append(q)

    else:

        st.number_input('Maximum Possible Score', value=27)

        critical_count = st.number_input(
            'Number of Critical Items',
            min_value=0,
            value=1
        )

        for i in range(int(critical_count)):
            label = st.text_input(f'Critical Item {i + 1} Label', key=f'cl{i}')

            st.markdown(f'**Critical Item {i + 1} Threshold**')
            st.markdown('*Minimum score on this item that will trigger a Safety Alert.*')
            threshold = st.number_input(
                '',
                key=f'ct{i}',
                value=1,
                label_visibility='collapsed'
            )

            critical_items.append({'label': label, 'threshold': threshold})

    st.subheader('Symptom Elevation Thresholds')

    st.markdown('**Low Upper Bound**')
    st.markdown('*Maximum total score classified as Low Symptom Elevation.*')
    low_max = st.number_input('Low Upper Bound', value=4, label_visibility='collapsed')

    st.markdown('**Moderate Upper Bound**')
    st.markdown('*Maximum total score classified as Moderate Symptom Elevation.*')
    mod_max = st.number_input('Moderate Upper Bound', value=14, label_visibility='collapsed')

    levels = {}

    for level_name, title, default_next in [
        ('low', 'Low Symptom Elevation', 'Monitoring recommended.'),
        ('moderate', 'Moderate Symptom Elevation', 'Further assessment recommended.'),
        ('high', 'Severe Symptom Elevation', 'Clinical follow-up strongly recommended.'),
        ('purple', 'Safety Alert', 'Immediate follow-up required.')
    ]:
        st.subheader(title)
        desc = st.text_area(f'{title} Description', key=f'd_{level_name}')
        next_steps = st.text_area(f'{title} Brief Next Steps', value=default_next, key=f'n_{level_name}')
        rec = st.text_area(f'{title} Detailed Recommendations & Resources', key=f'r_{level_name}')

        levels[level_name] = {
            'description': desc,
            'next_steps': next_steps,
            'recommendations': rec
        }

    st.subheader('Tool Summary')
    st.write(f'**Tool Name:** {tool_name}')
    st.write(f'**Focus Area:** {focus}')
    st.write(f'**Scoring Method:** {method}')

    if method == 'Questionnaire-Based Scoring':
        st.write(f'**Questions:** {len(questions)}')
    else:
        st.write(f'**Critical Items:** {len(critical_items)}')

    if not description:
        st.warning('Consider providing a description to assist future users.')

    st.subheader('Scoring Simulator')

    sim_score = st.number_input('Test Total Score', min_value=0, value=0, key='sim_score')
    sim_safety = st.checkbox('Simulate Safety Alert', key='sim_safety')

    if st.button('Run Simulation'):
        sim_level, sim_icon, sim_label = get_level(sim_score, low_max, mod_max)

        st.markdown(f'### {sim_icon} {sim_label}')
        st.write(f'**Total Score:** {sim_score}')
        st.write(levels[sim_level]['next_steps'])

        if sim_safety:
            st.markdown('# 🟣 SAFETY ALERT\n\n### Immediate Follow-Up Required')
            st.write(levels['purple']['next_steps'])

    if st.button('Save Tool') and tool_name:
        st.session_state.screening_tools[tool_name] = {
            'name': tool_name,
            'focus': focus,
            'description': description,
            'instructions': instructions,
            'method': method,
            'questions': questions,
            'critical_items': critical_items,
            'low_max': low_max,
            'mod_max': mod_max,
            'levels': levels,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        st.success('Tool saved.')

elif page == '📋 Use a Tool':

    if not st.session_state.screening_tools:
        st.info('No screening tools have been created yet.')
    else:
        name = st.selectbox('Select Tool', list(st.session_state.screening_tools.keys()))
        tool = st.session_state.screening_tools[name]

        if tool.get('description'):
            st.markdown(tool['description'])

        st.info(tool.get('instructions', ''))

        if tool.get('focus'):
            st.caption(f"Focus Area: {tool['focus']}")

        total = 0
        safety_alert = False

        if tool['method'] == 'Questionnaire-Based Scoring':
            for i, q in enumerate(tool['questions']):
                r = st.radio(q['text'], q.get('options', []), key=f'a{i}')
                score = q.get('scores', {}).get(r, 0)

                if q.get('reverse_scored'):
                    score = max(q['scores'].values()) - score

                total += score

                if q.get('safety_indicator') and r in q.get('trigger_responses', []):
                    safety_alert = True
        else:
            total = st.number_input('Total Score', value=0)

            for i, item in enumerate(tool.get('critical_items', [])):
                val = st.number_input(item['label'], value=0, key=f'ci{i}')
                if val >= item['threshold']:
                    safety_alert = True

        if st.button('Calculate Result'):
            level, icon, label = get_level(total, tool['low_max'], tool['mod_max'])

            st.markdown(f'## {icon} {label}')
            st.write(f'**Total Score:** {total}')

            if tool['levels'][level]['description']:
                st.write("**Interpretation:**")
                st.write(tool['levels'][level]['description'])

            st.markdown(
                f"**Next Steps:** {tool['levels'][level]['next_steps']}"
            )

            st.write('**Next Steps:**')
            st.write(tool['levels'][level]['next_steps'])

            with st.expander('View Recommendations'):
                st.write(tool['levels'][level]['recommendations'])

            if safety_alert:
                st.markdown('# 🟣 SAFETY ALERT\n\n### Immediate Follow-Up Required')
                st.markdown(f"**Next Steps:** {tool['levels']['purple']['next_steps']}")

                with st.expander('View Safety Alert Recommendations'):
                    st.write(tool['levels']['purple']['recommendations'])
            else:
                st.success('No Safety Alert Identified')

else:

    st.header('Manage Tools')
    st.caption('View tool definitions, inspect scoring structures, and export tool configurations.')

    if not st.session_state.screening_tools:
        st.info('No saved tools available.')

    for name, tool in st.session_state.screening_tools.items():
        with st.expander(name):
            st.json(tool)

            st.download_button(
                'Download Tool Definition',
                json.dumps(tool, indent=2),
                file_name=f'{name}.json',
                mime='application/json'
            )
