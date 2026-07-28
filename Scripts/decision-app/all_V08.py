import streamlit as st
from datetime import datetime

# ============= PAGE CONFIG =============
st.set_page_config(
    page_title="Mental Health Screening Tool Builder",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌱 Mental Health Screening Tool Builder")
st.markdown("*A simple tool for communities to create screening questionnaires that guide people toward local support.*")

# ============= SESSION STATE =============
if "screening_tools" not in st.session_state:
    st.session_state.screening_tools = {}
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ============= SIDEBAR NAVIGATION =============
page = st.sidebar.radio(
    "Choose what to do:",
    ["🏠 Home", "🛠️ Build Screening Tool", "📋 Use a Tool", "💾 Manage Tools"],
    label_visibility="collapsed"
)

# ============= PAGE 1: HOME =============
if page == "🏠 Home":
    st.markdown("""
    ### Welcome!

    This tool helps your community build simple mental health screening questionnaires.

    **What is a screening tool?**
    - A short set of questions that help identify if someone might need support
    - Results guide people toward appropriate local services (counseling, crisis lines, peer support, etc.)

    **How to use this app:**
    1. **Build a Tool** — Create screening questions based on evidence (from published screening tools like PHQ-9, GAD-7, etc.)
    2. **Use a Tool** — Answer questions and get results that suggest next steps
    3. **Manage Tools** — View, edit, or delete your screening tools

    ---
    ### Important Reminders
    - ⚠️ **This is a learning tool**, not for clinical use yet
    - Use validated questions when possible (consult published screening tools in your field)
    - Results should **always** guide people toward human support, not replace professional judgment
    - Avoid leading questions or assumptions about what's "right"
    """)

# ============= PAGE 2: BUILD SCREENING TOOL =============
elif page == "🛠️ Build Screening Tool":
    st.header("Build a New Screening Tool")

    # Templates to help users get started
    with st.expander("📚 See example templates (optional guidance)"):
        st.markdown("""
        **Common mental health screening areas:**
        - **Depression**: Sadness, hopelessness, loss of interest
        - **Anxiety**: Worry, panic, tension
        - **Substance use**: Frequency and impact of use
        - **Suicide risk**: Thoughts, plans, or intent to harm self
        - **Trauma**: Impact of difficult experiences

        **Tip:** For published screening tools, search for:
        - PHQ-9 (depression)
        - GAD-7 (anxiety)
        - AUDIT (substance use)
        - PCL-5 (trauma)
        """)

    st.divider()

    # Basic info
    col1, col2 = st.columns(2)
    with col1:
        tool_name = st.text_input(
            "Tool Name",
            placeholder="e.g., 'Depression Screening for Community Center'"
        )
    with col2:
        focus_area = st.selectbox(
            "What will this tool screen for?",
            ["Depression", "Anxiety", "Substance Use", "Trauma/PTSD", "Suicide Risk", "General Wellbeing", "Other"],
            index=None
        )

    tool_description = st.text_area(
        "Who is this for? (optional description)",
        placeholder="e.g., 'For our community health program, ages 18+, no prior diagnosis needed'",
        height=80
    )

    st.divider()
    st.subheader("Step 1: Add Questions")

    num_questions = st.number_input(
        "How many questions?",
        min_value=1,
        max_value=50,
        value=5,
        step=1
    )

    questions = []
    for i in range(num_questions):
        st.write(f"**Question {i+1}**")

        col1, col2 = st.columns([3, 1])
        with col1:
            q_text = st.text_input(
                f"Question {i+1}",
                placeholder="E.g., 'In the past 2 weeks, how often have you felt sad?'",
                key=f"q_text_{i}",
                label_visibility="collapsed"
            )
        with col2:
            q_type = st.selectbox(
                f"Answer type",
                ["Multiple Choice", "Yes/No", "Scale 0-10"],
                key=f"q_type_{i}",
                label_visibility="collapsed"
            )

        q_data = {"text": q_text, "type": q_type}

        # ========== Multiple Choice ==========
        if q_type == "Multiple Choice":
            options_text = st.text_input(
                f"Options (comma separated)",
                placeholder="Not at all, Several days, More than half the days, Nearly every day",
                key=f"q_options_{i}",
                label_visibility="collapsed"
            )
            options = [opt.strip() for opt in options_text.split(",") if opt.strip()]
            q_data["options"] = options

            st.caption("Optional: mark a specific response as a critical endorsement (Purple).")
            critical_triggers_text = st.text_input(
                "Critical trigger options (comma separated)",
                placeholder="e.g., Nearly every day",
                key=f"q_critical_triggers_{i}",
                label_visibility="collapsed"
            )
            critical_triggers = [opt.strip() for opt in critical_triggers_text.split(",") if opt.strip()]
            q_data["critical"] = {
                "enabled": len(critical_triggers) > 0,
                "triggers": critical_triggers
            }

            # --- Scoring for this question ---
            st.subheader("Scoring for this question")
            st.write("Assign points for each answer option. The app will sum points across all questions.")
            if options:
                option_points = {}
                cols = st.columns(2)
                with cols[0]:
                    st.caption("Option")
                with cols[1]:
                    st.caption("Points")

                for opt_idx, opt in enumerate(options):
                    row_cols = st.columns([3, 1])
                    with row_cols[0]:
                        st.write(opt)
                    with row_cols[1]:
                        pts = st.number_input(
                            f"pts_{i}_{opt_idx}",
                            min_value=0,
                            max_value=1000,
                            value=0,
                            step=1,
                            key=f"q_mc_pts_{i}_{opt_idx}",
                            label_visibility="collapsed"
                        )
                        option_points[opt] = int(pts)

                q_data["scoring"] = {
                    "type": "points_by_option",
                    "points_by_option": option_points
                }
            else:
                q_data["scoring"] = {
                    "type": "points_by_option",
                    "points_by_option": {}
                }

        # ========== Yes/No ==========
        elif q_type == "Yes/No":
            st.caption("Optional: mark 'Yes' or 'No' as a critical endorsement (Purple).")

            critical_yes = st.checkbox(
                "Treat YES as critical (Purple).",
                value=False,
                key=f"q_critical_yes_{i}"
            )

            q_data["critical"] = {
                "enabled": True if critical_yes else False,
                "yes_is_critical": critical_yes
            }

            # --- Scoring for this question ---
            st.subheader("Scoring for this question")
            st.write("Assign points for Yes and No answers. The app will sum points across all questions.")
            pts_yes = st.number_input(
                f"pts_yes_{i}",
                min_value=0,
                max_value=1000,
                value=2,
                step=1,
                key=f"q_yes_pts_{i}",
                label="Points for YES"
            )
            pts_no = st.number_input(
                f"pts_no_{i}",
                min_value=0,
                max_value=1000,
                value=0,
                step=1,
                key=f"q_no_pts_{i}",
                label="Points for NO"
            )

            q_data["scoring"] = {
                "type": "points_yes_no",
                "points_yes": int(pts_yes),
                "points_no": int(pts_no)
            }

        # ========== Scale 0-10 ==========
        elif q_type == "Scale 0-10":
            col_a, col_b = st.columns(2)
            with col_a:
                min_label = st.text_input(
                    "Label for 0",
                    value="Not at all",
                    key=f"q_min_label_{i}",
                    label_visibility="collapsed"
                )
            with col_b:
                max_label = st.text_input(
                    "Label for 10",
                    value="Extremely",
                    key=f"q_max_label_{i}",
                    label_visibility="collapsed"
                )
            q_data["min_label"] = min_label
            q_data["max_label"] = max_label

            st.caption("Optional: set a threshold that triggers critical endorsement (Purple).")
            critical_enabled = st.checkbox(
                "Enable Purple trigger for this question",
                value=False,
                key=f"q_critical_enable_{i}"
            )
            if critical_enabled:
                critical_threshold = st.slider(
                    "Critical trigger at or above value",
                    0, 10, 8,
                    key=f"q_critical_threshold_{i}"
                )
            else:
                critical_threshold = None

            q_data["critical"] = {
                "enabled": critical_enabled,
                "threshold": critical_threshold
            }

            # --- Scoring for this question ---
            st.subheader("Scoring for this question")
            st.write("Assign points for each value 0 through 10. The app will sum points across all questions.")

            # Keep this manageable in UI: show points in two columns.
            points_by_value = {}
            left_vals = list(range(0, 6))   # 0-5
            right_vals = list(range(6, 11)) # 6-10

            cols = st.columns(2)
            with cols[0]:
                st.caption("Values 0–5")
                for v in left_vals:
                    pts = st.number_input(
                        f"q_scale_pts_{i}_{v}",
                        min_value=0,
                        max_value=1000,
                        value=0,
                        step=1,
                        key=f"q_scale_pts_left_{i}_{v}",
                        label_visibility="collapsed"
                    )
                    points_by_value[v] = int(pts)
                    st.write(f"Value {v} → {int(pts)}")

            with cols[1]:
                st.caption("Values 6–10")
                for v in right_vals:
                    pts = st.number_input(
                        f"q_scale_pts_{i}_{v}",
                        min_value=0,
                        max_value=1000,
                        value=0,
                        step=1,
                        key=f"q_scale_pts_right_{i}_{v}",
                        label_visibility="collapsed"
                    )
                    points_by_value[v] = int(pts)
                    st.write(f"Value {v} → {int(pts)}")

            q_data["scoring"] = {
                "type": "points_by_value_0_to_10",
                "points_by_value": points_by_value
            }

        questions.append(q_data)
        st.divider()

    st.subheader("Step 2: Define Risk Levels & Referrals")

    st.write("""
    Overall triage is determined by **total score** (Green/Yellow/Red).
    
    Separately, some answers can also trigger **Purple = Imminent Safety Risk** (critical endorsement),
    which is independent of the overall triage.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**🟢 Green - Low Risk**")
        low_description = st.text_area(
            "What does this mean?",
            value="Minimal signs of concern at this time.",
            key="low_desc",
            height=100
        )
        low_referral = st.text_area(
            "What should they do?",
            value="Continue healthy habits. Resources available if needed.",
            key="low_referral",
            height=100
        )

    with col2:
        st.write("**🟡 Yellow - Moderate Risk**")
        moderate_description = st.text_area(
            "What does this mean?",
            value="Some signs of concern that warrant attention.",
            key="moderate_desc",
            height=100
        )
        moderate_referral = st.text_area(
            "What should they do?",
            value="Schedule an appointment with a counselor or therapist. Call: [Local mental health line]",
            key="moderate_referral",
            height=100
        )

    with col3:
        st.write("**🔴 Red - High Risk**")
        high_description = st.text_area(
            "What does this mean?",
            value="Significant concern requiring urgent support.",
            key="high_desc",
            height=100
        )
        high_referral = st.text_area(
            "What should they do?",
            value="⚠️ Reach out now. Crisis Line: [24/7 number]. Tell someone you trust. Go to nearest ER if in danger.",
            key="high_referral",
            height=100
        )

    st.divider()

    st.subheader("Purple: Imminent Safety Risk (independent critical flag)")
    purple_col1, purple_col2 = st.columns(2)
    with purple_col1:
        purple_description = st.text_area(
            "Purple label description (what does it mean?)",
            value="Critical endorsement suggesting immediate safety concerns.",
            key="purple_desc",
            height=100
        )
    with purple_col2:
        purple_referral = st.text_area(
            "Purple recommendations (what should they do?)",
            value="⚠️ Treat as urgent. Contact a crisis line or emergency services now. If someone is in immediate danger, call emergency services (e.g., 911) or go to the nearest ER.",
            key="purple_referral",
            height=100
        )

    st.divider()

    st.subheader("Step 3: Scoring & Cutoffs (total score → triage)")

    st.write("This section is flexible: whatever points you assign to each answer will be summed, and then total score ranges decide Green/Yellow/Red.")

    st.caption("Example (just to show the concept): If total score is 0–7 → Green, 8–14 → Yellow, 15+ → Red.")

    # Cutoffs by total score ranges
    colA, colB, colC = st.columns(3)

    with colA:
        st.write("**Green cutoff (inclusive)**")
        green_min = st.number_input(
            "Green min total score",
            min_value=0,
            max_value=1000000,
            value=0,
            step=1,
            key="green_min"
        )
        green_max = st.number_input(
            "Green max total score (inclusive)",
            min_value=0,
            max_value=1000000,
            value=7,
            step=1,
            key="green_max"
        )

    with colB:
        st.write("**Yellow cutoff (inclusive)**")
        yellow_min = st.number_input(
            "Yellow min total score",
            min_value=0,
            max_value=1000000,
            value=8,
            step=1,
            key="yellow_min"
        )
        yellow_max = st.number_input(
            "Yellow max total score (inclusive)",
            min_value=0,
            max_value=1000000,
            value=14,
            step=1,
            key="yellow_max"
        )

    with colC:
        st.write("**Red cutoff**")
        red_min = st.number_input(
            "Red min total score (inclusive)",
            min_value=0,
            max_value=1000000,
            value=15,
            step=1,
            key="red_min"
        )
        red_max = st.number_input(
            "Red max total score (optional; leave high for '15+')",
            min_value=0,
            max_value=1000000,
            value=1000000,
            step=1,
            key="red_max"
        )

    # Basic user-friendly examples panel
    with st.expander("✅ Help me enter scoring correctly (examples)"):
        st.markdown("""
        **Valid patterns (examples):**
        - **Points per answer, then total mapping**
          - Multiple choice: "Not at all" = 0, "Several days" = 1, "Nearly every day" = 3
          - Total: Green 0–7, Yellow 8–14, Red 15+
        - **Scale 0–10 with custom point mapping**
          - Value 0–2 → 0 points
          - Value 3–6 → 1 point
          - Value 7–10 → 3 points
        - **Yes/No weighting**
          - YES = 2 points, NO = 0 points
        """)

    # Save button (stores structured scoring + cutoffs)
    if st.button("💾 Save This Screening Tool", type="primary", use_container_width=True):
        def is_nonempty_str(x):
            return isinstance(x, str) and x.strip() != ""

        errors = []

        if not is_nonempty_str(tool_name):
            errors.append("Tool name is required.")
        if not questions:
            errors.append("At least one question is required.")

        # Validate each question
        for idx, q in enumerate(questions, start=1):
            if not is_nonempty_str(q.get("text", "")):
                errors.append(f"Question {idx}: question text is required.")

            q_type = q.get("type")

            if q_type == "Multiple Choice":
                opts = q.get("options", [])
                if not opts:
                    errors.append(f"Question {idx}: at least one option is required for Multiple Choice.")
                scoring = q.get("scoring", {})
                if scoring.get("type") != "points_by_option":
                    errors.append(f"Question {idx}: scoring not configured for Multiple Choice.")
                pb = scoring.get("points_by_option", {})
                # Ensure every option has points entry
                for opt in opts:
                    if opt not in pb:
                        errors.append(f"Question {idx}: scoring points missing for option '{opt}'.")

            elif q_type == "Yes/No":
                scoring = q.get("scoring", {})
                if scoring.get("type") != "points_yes_no":
                    errors.append(f"Question {idx}: scoring not configured for Yes/No.")
                if "points_yes" not in scoring or "points_no" not in scoring:
                    errors.append(f"Question {idx}: scoring points for Yes/No are required.")

            elif q_type == "Scale 0-10":
                scoring = q.get("scoring", {})
                if scoring.get("type") != "points_by_value_0_to_10":
                    errors.append(f"Question {idx}: scoring not configured for Scale 0–10.")
                pb = scoring.get("points_by_value", {})
                for v in range(0, 11):
                    if v not in pb:
                        errors.append(f"Question {idx}: scoring points missing for value '{v}' (0–10).")

            else:
                errors.append(f"Question {idx}: unknown question type.")

        # Validate cutoff ranges ordering
        green_min_i = int(green_min)
        green_max_i = int(green_max)
        yellow_min_i = int(yellow_min)
        yellow_max_i = int(yellow_max)
        red_min_i = int(red_min)
        red_max_i = int(red_max)

        if green_max_i < green_min_i:
            errors.append("Green max total score must be >= green min total score.")
        if yellow_max_i < yellow_min_i:
            errors.append("Yellow max total score must be >= yellow min total score.")
        if red_max_i < red_min_i:
            errors.append("Red max total score must be >= red min total score.")

        # Ensure cutoffs don't overlap or leave gaps is optional; we’ll warn via errors if they overlap.
        # (We keep it strict so results are predictable.)
        overlaps = []
        def intersects(a1, a2, b1, b2):
            return max(a1, b1) <= min(a2, b2)

        if intersects(green_min_i, green_max_i, yellow_min_i, yellow_max_i):
            overlaps.append("Green and Yellow ranges overlap.")
        if intersects(green_min_i, green_max_i, red_min_i, red_max_i):
            overlaps.append("Green and Red ranges overlap.")
        if intersects(yellow_min_i, yellow_max_i, red_min_i, red_max_i):
            overlaps.append("Yellow and Red ranges overlap.")

        if overlaps:
            errors.extend(overlaps)

        if errors:
            st.error("❌ Please fix before saving:\n" + "\n".join(errors))
        else:
            st.session_state.screening_tools[tool_name] = {
                "name": tool_name,
                "focus_area": focus_area,
                "description": tool_description,
                "questions": questions,
                "risk_levels": {
                    "low": {"label": "Green (Low Risk)", "description": low_description, "referral": low_referral},
                    "moderate": {"label": "Yellow (Moderate Risk)", "description": moderate_description, "referral": moderate_referral},
                    "high": {"label": "Red (High Risk)", "description": high_description, "referral": high_referral},
                    "purple": {"label": "Purple (Imminent Safety Risk)", "description": purple_description, "referral": purple_referral},
                },
                "scoring": {
                    "cutoffs": {
                        "green": {"min": green_min_i, "max": green_max_i},
                        "yellow": {"min": yellow_min_i, "max": yellow_max_i},
                        "red": {"min": red_min_i, "max": red_max_i},
                    }
                },
                "created": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.success(f"✅ Saved: **{tool_name}**")
            st.balloons()

# ============= PAGE 3: USE A TOOL =============
elif page == "📋 Use a Tool":
    st.header("Answer Screening Questions")

    if not st.session_state.screening_tools:
        st.info("📭 No screening tools built yet. Go to **Build Screening Tool** to create one.")
    else:
        tool_name = st.selectbox(
            "Select a tool to use:",
            list(st.session_state.screening_tools.keys()),
            label_visibility="visible"
        )

        if tool_name:
            tool = st.session_state.screening_tools[tool_name]

            st.subheader(tool_name)
            st.write(f"**Screens for:** {tool.get('focus_area', 'General wellbeing')}")
            if tool.get("description"):
                st.write(f"*{tool['description']}*")

            st.divider()
            st.write("### Please answer the following questions:")
            st.info("Your answers are private. Results are for your information only.")

            responses = []
            total_score = 0
            purple_triggers_hit = []

            for i, question in enumerate(tool["questions"]):
                st.write(f"**{i+1}. {question['text']}**")

                q_type = question["type"]

                if q_type == "Multiple Choice":
                    response = st.radio(
                        f"Q{i+1}",
                        question.get("options", []),
                        key=f"response_{i}",
                        label_visibility="collapsed"
                    )
                    responses.append(response)

                    scoring = question.get("scoring", {}) or {}
                    pts = 0
                    if scoring.get("type") == "points_by_option":
                        pts = int(scoring.get("points_by_option", {}).get(response, 0))
                    total_score += pts

                    crit = question.get("critical", {}) or {}
                    if response and crit.get("enabled") and response in (crit.get("triggers", []) or []):
                        purple_triggers_hit.append(i)

                elif q_type == "Yes/No":
                    response = st.radio(
                        f"Q{i+1}",
                        ["Yes", "No"],
                        key=f"response_{i}",
                        label_visibility="collapsed"
                    )
                    responses.append(response)

                    scoring = question.get("scoring", {}) or {}
                    pts = 0
                    if scoring.get("type") == "points_yes_no":
                        pts = int(scoring.get("points_yes", 0)) if response == "Yes" else int(scoring.get("points_no", 0))
                    total_score += pts

                    crit = question.get("critical", {}) or {}
                    if crit.get("enabled") and response == "Yes" and crit.get("yes_is_critical", False) is True:
                        purple_triggers_hit.append(i)

                elif q_type == "Scale 0-10":
                    response = st.slider(
                        f"Q{i+1}",
                        0, 10,
                        value=5,
                        key=f"response_{i}",
                        label_visibility="collapsed"
                    )
                    responses.append(response)
                    scoring = question.get("scoring", {}) or {}
                    pts = 0
                    if scoring.get("type") == "points_by_value_0_to_10":
                        pts = int(scoring.get("points_by_value", {}).get(int(response), 0))
                    total_score += pts

                    crit = question.get("critical", {}) or {}
                    if crit.get("enabled") and crit.get("threshold") is not None:
                        if int(response) >= int(crit["threshold"]):
                            purple_triggers_hit.append(i)

                st.divider()

            # Determine triage based on total score cutoffs (Green/Yellow/Red)
            cutoffs = (tool.get("scoring", {}) or {}).get("cutoffs", {}) or {}
            green = cutoffs.get("green", {"min": 0, "max": 0})
            yellow = cutoffs.get("yellow", {"min": 0, "max": 0})
            red = cutoffs.get("red", {"min": 0, "max": 0})

            def in_range(x, r):
                return int(r["min"]) <= int(x) <= int(r["max"])

            if in_range(total_score, green):
                risk_level = "low"
                icon = "🟢"
            elif in_range(total_score, yellow):
                risk_level = "moderate"
                icon = "🟡"
            elif in_range(total_score, red):
                risk_level = "high"
                icon = "🔴"
            else:
                # If someone enters inconsistent ranges, pick the closest sensible fallback.
                # (But ranges are validated on save; this is just a guard.)
                risk_level = "moderate"
                icon = "🟡"

            # Purple independent flag
            purple_enabled = len(purple_triggers_hit) > 0

            if st.button("📊 See My Results", type="primary", use_container_width=True):
                st.session_state.last_result = {
                    "tool": tool_name,
                    "responses": responses,
                    "triage_level": risk_level,
                    "triage_score": total_score,
                    "purple_flag": purple_enabled,
                    "purple_triggers": purple_triggers_hit,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                }

                st.divider()
                st.markdown(f"## {icon} Your Overall Triage: {tool['risk_levels'][risk_level]['label']}")
                triage_info = tool["risk_levels"][risk_level]
                st.write(f"**Total score:** {total_score}")
                st.write(f"**What this means:** {triage_info['description']}")
                st.divider()

                st.markdown("### ➜ Next Steps (Overall Triaged Guidance)")
                st.write(triage_info["referral"])

                st.divider()
                if purple_enabled:
                    st.markdown("## 🟣 Purple: Imminent Safety Risk (Critical Flag Triggered)")
                    purple_info = tool["risk_levels"]["purple"]
                    st.write(f"**What this means:** {purple_info['description']}")
                    st.divider()
                    st.markdown("### ➜ Next Steps (Immediate Safety Guidance)")
                    st.error(purple_info["referral"])
                    st.caption(f"Critical trigger(s) from question number(s): {[i+1 for i in purple_triggers_hit]}")
                else:
                    st.markdown("## 🟣 Purple: Not triggered")
                    st.caption("No configured critical endorsements were selected.")

                st.divider()
                st.write(f"*Result saved: {st.session_state.last_result['timestamp']}*")

# ============= PAGE 4: MANAGE TOOLS =============
elif page == "💾 Manage Tools":
    st.header("Your Screening Tools")

    if not st.session_state.screening_tools:
        st.info("📭 No tools saved yet. Build your first one!")
    else:
        for tool_name, tool in st.session_state.screening_tools.items():
            with st.expander(f"📋 {tool_name}"):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write(f"**Screens for:** {tool.get('focus_area', 'General')}")
                    if tool.get("description"):
                        st.write(f"**Description:** {tool['description']}")
                    st.write(f"**Questions:** {len(tool['questions'])}")
                    st.write(f"**Created:** {tool.get('created', 'Unknown')}")

                    with st.expander("View full details"):
                        st.write("**Questions:**")
                        for i, q in enumerate(tool["questions"], 1):
                            st.write(f"{i}. {q['text']} (type: {q['type']})")
                            if q.get("critical", {}) and q["critical"].get("enabled"):
                                st.write(f"   - Purple trigger enabled: {q['critical']}")

                            st.write(f"   - Scoring config: {q.get('scoring', {})}")

                        st.write("**Overall triage cutoffs (total score):**")
                        st.write(tool.get("scoring", {}).get("cutoffs", {}))

                        st.write("**Scoring rules overview:**")
                        st.write("Points are assigned per answer; the app sums total score and uses cutoffs to select Green/Yellow/Red.")

                with col2:
                    if st.button("🗑️ Delete", key=f"delete_{tool_name}"):
                        del st.session_state.screening_tools[tool_name]
                        st.rerun()

        st.divider()
        st.subheader("Last Result")
        if st.session_state.last_result:
            result = st.session_state.last_result
            st.write(f"**Tool:** {result['tool']}")
            st.write(f"**Overall triage:** {result['triage_level'].upper()}")
            st.write(f"**Total score:** {result['triage_score']}")
            st.write(f"**Purple flag:** {'YES' if result['purple_flag'] else 'NO'}")
            st.write(f"**Timestamp:** {result['timestamp']}")
        else:
            st.write("No results yet.")
