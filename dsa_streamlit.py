import streamlit as st
import pandas as pd
import datetime
import uuid
import copy
import json
import os

st.set_page_config(page_title="DSA Daily Scheduler", layout="wide")

DATA_FILENAME = "dsa_schedule.json"

def date_fmt(dt):
    if isinstance(dt, pd.Timestamp):
        dt = dt.date()
    return dt.strftime('%d/%m/%y')

def daterange_fmt(start, end):
    if isinstance(start, pd.Timestamp):
        start = start.date()
    if isinstance(end, pd.Timestamp):
        end = end.date()
    if start == end:
        return date_fmt(start)
    return f"{date_fmt(start)} – {date_fmt(end)}"

def parse_date(s):
    try:
        return datetime.datetime.strptime(s, "%d/%m/%y").date()
    except Exception:
        return None

def days_between(start, end):
    if isinstance(start, pd.Timestamp):
        start = start.date()
    if isinstance(end, pd.Timestamp):
        end = end.date()
    return (end - start).days + 1

def get_uid():
    return str(uuid.uuid4())

def next_day(d):
    if isinstance(d, pd.Timestamp):
        d = d.date()
    return d + datetime.timedelta(days=1)

def prev_day(d):
    if isinstance(d, pd.Timestamp):
        d = d.date()
    return d - datetime.timedelta(days=1)

# Persistence helpers

def save_data_to_file():
    try:
        with open(DATA_FILENAME, "w") as f:
            json.dump(st.session_state.dsa_sheet, f, default=str)
    except Exception as e:
        st.error(f"Error saving data: {e}")

def load_data_from_file():
    if os.path.exists(DATA_FILENAME):
        try:
            with open(DATA_FILENAME, "r") as f:
                data = json.load(f)
                return data
        except Exception as e:
            st.error(f"Error loading data: {e}")
    return None

# Full original DEFAULT_DATA from your initial code (with proper dates & UIDs)
DEFAULT_DATA = [
    {"Type": "DSA", "Topic": "LinkedList", "Days": 9, "Date Range": "27/07/25 – 04/08/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Recursion", "Days": 6, "Date Range": "05/08/25 – 10/08/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Bit Manipulation (Part 1)", "Days": 3, "Date Range": "11/08/25 – 13/08/25", "Notes": "", "UID": get_uid()},
    {"Type": "Break", "Topic": "CAT-1", "Days": 12, "Date Range": "14/08/25 – 25/08/25", "Notes": "🧠 Exams", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Bit Manipulation (Part 2)", "Days": 2, "Date Range": "26/08/25 – 27/08/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Stack & Queues", "Days": 7, "Date Range": "28/08/25 – 03/09/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Sliding Window", "Days": 6, "Date Range": "04/09/25 – 09/09/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Heaps", "Days": 5, "Date Range": "10/09/25 – 14/09/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Greedy Algorithms", "Days": 7, "Date Range": "15/09/25 – 24/09/25", "Notes": "", "UID": get_uid()},
    {"Type": "Break", "Topic": "Gravitas", "Days": 5, "Date Range": "25/09/25 – 29/09/25", "Notes": "🎓 Event", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Binary Trees (Part 1)", "Days": 2, "Date Range": "30/09/25 – 01/10/25", "Notes": "", "UID": get_uid()},
    {"Type": "Break", "Topic": "CAT-2", "Days": 12, "Date Range": "02/10/25 – 13/10/25", "Notes": "🧠 Exams", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Binary Trees (Part 2)", "Days": 10, "Date Range": "14/10/25 – 16/10/25, 19/10/25 – 25/10/25", "Notes": "", "UID": get_uid()},
    {"Type": "Break", "Topic": "Diwali Travel 1", "Days": 2, "Date Range": "17/10/25 – 18/10/25", "Notes": "🪔 Festival", "UID": get_uid()},
    {"Type": "Break", "Topic": "Diwali Travel 2", "Days": 2, "Date Range": "26/10/25 – 27/10/25", "Notes": "🛫 Travel", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Binary Search Trees", "Days": 3, "Date Range": "28/10/25 – 30/10/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Graphs (Part 1)", "Days": 5, "Date Range": "31/10/25 – 05/11/25", "Notes": "", "UID": get_uid()},
    {"Type": "Break", "Topic": "FAT & Labs + FAT", "Days": 31, "Date Range": "06/11/25 – 06/12/25", "Notes": "📚 Exams", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Graphs (Part 2)", "Days": 9, "Date Range": "07/12/25 – 15/12/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Dynamic Programming", "Days": 16, "Date Range": "16/12/25 – 31/12/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Tries", "Days": 5, "Date Range": "01/01/26 – 05/01/26", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Strings", "Days": 7, "Date Range": "06/01/26 – 12/01/26", "Notes": "", "UID": get_uid()},
]

if "dsa_sheet" not in st.session_state:
    loaded = load_data_from_file()
    if loaded:
        st.session_state.dsa_sheet = loaded
    else:
        st.session_state.dsa_sheet = copy.deepcopy(DEFAULT_DATA)

def expand_date_ranges(row):
    drs = row["Date Range"].split(",")
    ranges = []
    for dr in drs:
        dr = dr.strip()
        if "–" in dr:
            parts = dr.split("–")
            start = parse_date(parts[0].strip())
            end = parse_date(parts[1].strip())
        else:
            start = end = parse_date(dr)
        if start and end:
            ranges.append((start, end))
    return ranges

def intervals_overlap(start1, end1, start2, end2):
    return start1 <= end2 and start2 <= end1

def split_interval_by_interval(outer_start, outer_end, inner_start, inner_end):
    result = []
    if inner_start > outer_start:
        result.append((outer_start, prev_day(inner_start)))
    if inner_end < outer_end:
        result.append((next_day(inner_end), outer_end))
    return result

def reschedule_with_interruptions(entries, new_topic=None, delete_uid=None):
    events = copy.deepcopy(entries)
    if delete_uid:
        events = [e for e in events if e['UID'] != delete_uid]

    breaks = [e for e in events if e["Type"] == "Break"]
    dsa = [e for e in events if e["Type"] == "DSA"]

    break_intervals = []
    for br in breaks:
        for bstart, bend in expand_date_ranges(br):
            break_intervals.append((bstart, bend))
    break_intervals.sort()

    new_topic_range = None
    if new_topic:
        new_topic_range = (new_topic['start'], new_topic['end'])

    split_chunks = []

    def get_earliest_start(ev):
        starts = [s for s, e in expand_date_ranges(ev)]
        return min(starts) if starts else datetime.date.today()
    dsa_sorted = sorted(dsa, key=get_earliest_start)

    for topic in dsa_sorted:
        topic_ranges = expand_date_ranges(topic)

        topic_segments = []

        for tstart, tend in topic_ranges:
            if new_topic_range and intervals_overlap(tstart, tend, new_topic_range[0], new_topic_range[1]):
                split_before_after = split_interval_by_interval(tstart, tend, new_topic_range[0], new_topic_range[1])
            else:
                split_before_after = [(tstart, tend)]

            for seg_start, seg_end in split_before_after:
                if seg_start > seg_end:
                    continue

                current_start = seg_start
                while current_start <= seg_end:
                    next_break = None
                    for bstart, bend in break_intervals:
                        if bstart <= seg_end and bend >= current_start:
                            if bstart > current_start:
                                free_seg_end = prev_day(bstart)
                            else:
                                current_start = next_day(bend)
                                break
                            next_break = (bstart, bend)
                            break
                    else:
                        free_seg_end = seg_end
                        next_break = None

                    if current_start <= free_seg_end:
                        topic_segments.append((current_start, free_seg_end))
                        current_start = next_day(free_seg_end)
                    else:
                        if next_break is None:
                            break
                        current_start = next_day(next_break[1])

        topic_segments = sorted(topic_segments)
        total_parts = len(topic_segments)
        for idx, (ps, pe) in enumerate(topic_segments, 1):
            days_len = days_between(ps, pe)
            uid = get_uid()
            display_topic = topic['Topic']
            if total_parts > 1:
                display_topic = f"{display_topic} (part {idx} of {total_parts})"

            split_chunks.append({
                "Type": "DSA",
                "Topic": display_topic,
                "Days": days_len,
                "Date Range": daterange_fmt(ps, pe),
                "Notes": topic.get("Notes", ""),
                "UID": uid,
                "OrigUID": topic.get("UID"),
                "Start": ps,
                "End": pe,
            })

    if new_topic:
        days_len = days_between(new_topic['start'], new_topic['end'])
        split_chunks.append({
            "Type": "DSA",
            "Topic": new_topic['topic'],
            "Days": days_len,
            "Date Range": daterange_fmt(new_topic['start'], new_topic['end']),
            "Notes": new_topic.get("note", ""),
            "UID": get_uid(),
            "Start": new_topic['start'],
            "End": new_topic['end'],
        })

    for br in breaks:
        ranges = expand_date_ranges(br)
        for bstart, bend in ranges:
            days_len = days_between(bstart, bend)
            split_chunks.append({
                "Type": "Break",
                "Topic": br["Topic"],
                "Days": days_len,
                "Date Range": daterange_fmt(bstart, bend),
                "Notes": br.get("Notes", ""),
                "UID": br.get("UID", get_uid()),
                "Start": bstart,
                "End": bend,
            })

    split_chunks.sort(key=lambda x: x["Start"])

    consolidated = []
    for seg in split_chunks:
        if consolidated:
            last = consolidated[-1]
            if (seg["Type"] == last["Type"] and seg["Topic"] == last["Topic"] and
                (last["End"] + datetime.timedelta(days=1)) == seg["Start"]):
                last["End"] = seg["End"]
                last["Days"] = days_between(last["Start"], last["End"])
                last["Date Range"] = daterange_fmt(last["Start"], last["End"])
                continue
        consolidated.append(seg)

    topic_groups = {}
    for ev in consolidated:
        key = (ev["Type"], ev["Topic"])
        topic_groups.setdefault(key, []).append(ev)

    topic_order = sorted(topic_groups.keys(), key=lambda k: min(ev["Start"] for ev in topic_groups[k]))

    result = []
    for group_idx, grp_key in enumerate(topic_order, 1):
        evs = topic_groups[grp_key]
        if grp_key[0] == "DSA":
            total_parts = len(evs)
            for part_idx, ev in enumerate(evs, 1):
                base_topic = ev["Topic"].split(" (part ")[0].strip()
                if total_parts > 1:
                    ev["Topic"] = f"{base_topic} ({part_idx} of {total_parts})"
                else:
                    ev["Topic"] = base_topic
                ev["S No."] = f"{group_idx}.{part_idx}"
                result.append(ev)
        else:
            ev = evs[0]
            ev["S No."] = str(group_idx)
            result.append(ev)

    return result

def main():
    st.title("📅 DSA Daily Scheduler with Persistence & Interruptions")

    st.info(
        "Add new DSA study topics to split existing overlapping topics appropriately.\n"
        "Breaks remain fixed.\n"
        "Your schedule is saved locally and changes persist on refresh.\n"
        "Delete rows or add new entries to update your schedule instantly."
    )

    st.session_state.dsa_sheet = reschedule_with_interruptions(st.session_state.dsa_sheet)
    df = pd.DataFrame(st.session_state.dsa_sheet)

    if not df.empty:
        st.subheader("DSA Schedule Table")
        st.dataframe(df.drop(columns=["UID", "Start", "End"]), use_container_width=True)

        st.markdown("### Delete any row:")
        for idx, row in df.iterrows():
            col1, col2 = st.columns([9, 1])
            col1.markdown(f"**{row['S No.']} {row['Type']} — {row['Topic']}** ({row['Date Range']})")
            if col2.button("🗑️ Delete", key=f"del_{row['UID']}"):
                st.session_state.dsa_sheet = reschedule_with_interruptions(st.session_state.dsa_sheet, delete_uid=row['UID'])
                save_data_to_file()
                st.rerun()
                return
    else:
        st.info("No DSA schedule entries yet.")

    st.markdown("---")
    st.subheader("Add Study Topic")

    today = datetime.date.today()

    with st.form("add_study_form"):
        study_topic = st.text_input("Topic (e.g. LinkedList)", value="", key="input_topic")
        study_from = st.date_input("From Date", value=today, key="input_from")
        study_to = st.date_input("To Date", value=today, key="input_to")
        study_notes = st.text_input("Notes (optional)", value="✅ Manually Added", key="input_note")
        submitted = st.form_submit_button("➕ Add Study Topic")

    if submitted:
        if not study_topic.strip():
            st.error("Please enter a study topic.")
        elif study_from > study_to:
            st.error("From date cannot be after To date.")
        else:
            new_topic_input = {
                "topic": study_topic.strip(),
                "start": study_from,
                "end": study_to,
                "note": study_notes.strip(),
            }
            st.session_state.dsa_sheet = reschedule_with_interruptions(st.session_state.dsa_sheet, new_topic=new_topic_input)
            save_data_to_file()
            st.success(f"Added study topic '{study_topic.strip()}' and rescheduled.")
            st.rerun()
            return

    st.markdown("---")
    st.markdown("Made with ❤️ for efficient DSA prep!")

# Run main at top-level for Streamlit
main()
