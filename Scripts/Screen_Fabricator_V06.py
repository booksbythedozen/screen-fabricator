import streamlit as st
from datetime import datetime

st.set_page_config(page_title='Screen Fabricator V06', layout='wide')

st.title('🧩 Screen Fabricator V06')
st.caption('Created by Bryce P Mulligan, PhD, CPsych')
st.markdown('*Faster Tool Creation. Clearer Clinical Guidance.*')

if 'screening_tools' not in st.session_state:
    st.session_state.screening_tools = {}


def get_level(score, low_max, mod_max):
    if score <= low_max:
        return 'low', '🟢', 'Low Symptom Elevation'
    elif score <= mod_max:
        return 'moderate', '🟡', 'Moderate Symptom Elevation'
    return 'high', '🔴', 'High Symptom Elevation'

page = st.sidebar.radio('Navigation', ['🏠 Home','🛠️ Build Screening Tool','📋 Use a Tool','💾 Manage Tools'])

if page == '🏠 Home':
    st.header('Welcome')
    st.write('Create, test, and administer custom mental health screening and triage workflows.')

elif page == '🛠️ Build Screening Tool':
    tool_name = st.text_input('Tool Name')
    focus = st.text_input('Focus Area')
    description = st.text_area('Description')
    instructions = st.text_area('Instructions for Respondents')

    method = st.radio('Scoring Method', ['Questionnaire-Based Scoring', 'Total Score Entry'])

    questions = []
    critical_items = []
    shared_template = None

    if method == 'Questionnaire-Based Scoring':
        response_mode = st.radio('Response Structure', ['Use same response options for all items', 'Custom response options per item'])

        if response_mode == 'Use same response options for all items':
            st.subheader('Shared Response Template')
            raw = st.text_input('Options (comma separated)', value='Not at all, Several days, More than half the days, Nearly every day')
            opts = [x.strip() for x in raw.split(',') if x.strip()]
            scores = {}
            for opt in opts:
                scores[opt] = st.number_input(f'Score for {opt}', value=max(0, opts.index(opt)), key=f'temp_{opt}')
            shared_template = {'options': opts, 'scores': scores}

        n = st.number_input('Number of Questions', min_value=1, value=9)

        for i in range(int(n)):
            st.subheader(f'Question {i+1}')
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
                    scores[opt] = st.number_input(f'Score: {opt}', value=0, key=f's_{i}_{opt}')
                q['options'] = opts
                q['scores'] = scores

            q['reverse_scored'] = st.checkbox('Reverse Scored', key=f'rev_{i}')
            q['safety_indicator'] = st.checkbox(
                'Safety Indicator',
                help='Check if a response should trigger a Safety Alert regardless of overall score.',
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
        max_score = st.number_input('Maximum Possible Score', value=27)
        critical_count = st.number_input('Number of Critical Items', min_value=0, value=1)
        for i in range(int(critical_count)):
            label = st.text_input(f'Critical Item {i+1} Label', key=f'cl{i}')
            threshold = st.number_input(f'Critical Item {i+1} Threshold', key=f'ct{i}', value=1)
            critical_items.append({'label': label, 'threshold': threshold})

    st.subheader('Symptom Elevation Thresholds')
    low_max = st.number_input('Low Upper Bound', value=4)
    mod_max = st.number_input('Moderate Upper Bound', value=14)

    levels = {}
    for level_name, title, default_next in [
        ('low','Low Symptom Elevation','Monitoring recommended.'),
        ('moderate','Moderate Symptom Elevation','Further assessment recommended.'),
        ('high','High Symptom Elevation','Clinical follow-up strongly recommended.'),
        ('purple','Safety Alert','Immediate follow-up required.')]:

        st.subheader(title)
        desc = st.text_area(f'{title} Description', key=f'd_{level_name}')
        next_steps = st.text_area(f'{title} Brief Next Steps', value=default_next, key=f'n_{level_name}')
        rec = st.text_area(f'{title} Detailed Recommendations & Resources', key=f'r_{level_name}')
        levels[level_name] = {'description': desc, 'next_steps': next_steps, 'recommendations': rec}

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
    if st.session_state.screening_tools:
        name = st.selectbox('Select Tool', list(st.session_state.screening_tools.keys()))
        tool = st.session_state.screening_tools[name]
        st.info(tool.get('instructions', ''))

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
            st.markdown(f"**Next Steps:** {tool['levels'][level]['next_steps']}")
            with st.expander('View Recommendations'):
                st.write(tool['levels'][level]['recommendations'])

            if safety_alert:
                st.error('🟣 SAFETY ALERT')
                st.markdown(f"**Next Steps:** {tool['levels']['purple']['next_steps']}")
                with st.expander('View Safety Alert Recommendations'):
                    st.write(tool['levels']['purple']['recommendations'])
            else:
                st.success('No Safety Alert Identified')

else:
    st.header('Manage Tools')
    for name, tool in st.session_state.screening_tools.items():
        with st.expander(name):
            st.json(tool)
