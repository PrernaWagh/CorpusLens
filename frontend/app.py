import streamlit as st
import subprocess
import tempfile
import os
import re
from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

SEQUENTIAL = ROOT / "sequential"
PARALLEL = ROOT / "parallel"
PLOTS = ROOT / "results" / "plots"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CorpusLens",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("📚 CorpusLens")
st.markdown(
    """
    **Corpus Analysis and Parallel Processing Dashboard**

    Upload a text corpus and analyze its statistics, word frequencies,
    sequential execution, parallel execution, and performance.
    """
)

st.divider()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def parse_output(output):
    """
    Parse statistics and top-frequency words from the C++ output.
    """

    stats = {}
    top_words = []

    patterns = {
        "total_lines": r"Total lines\s*:\s*([\d.]+)",
        "total_paragraphs": r"Total paragraphs\s*:\s*([\d.]+)",
        "total_words": r"Total words\s*:\s*([\d.]+)",
        "unique_words": r"Unique words\s*:\s*([\d.]+)",
        "total_characters": r"Total characters\s*:\s*([\d.]+)",
        "total_sentences": r"Total sentences\s*:\s*([\d.]+)",
        "avg_words_line": r"Average words/line\s*:\s*([\d.]+)",
        "avg_words_sentence": r"Average words/sentence\s*:\s*([\d.]+)",
        "avg_characters_line": r"Average characters/line\s*:\s*([\d.]+)",
        "threads": r"Threads\s*:\s*(\d+)",
        "execution_time": r"Execution time\s*:\s*([\d.]+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, output)

        if match:
            value = match.group(1)

            if key in {
                "avg_words_line",
                "avg_words_sentence",
                "avg_characters_line",
                "execution_time"
            }:
                stats[key] = float(value)
            else:
                stats[key] = int(float(value))

    # Parse top frequent words
    in_top_words = False

    for line in output.splitlines():

        if "TOP FREQUENT WORDS" in line:
            in_top_words = True
            continue

        if in_top_words:

            match = re.match(
                r"\s*(\d+)\s+(\S+)\s+(\d+)",
                line
            )

            if match:
                rank = int(match.group(1))
                word = match.group(2)
                frequency = int(match.group(3))

                top_words.append(
                    {
                        "Rank": rank,
                        "Word": word,
                        "Frequency": frequency
                    }
                )

    return stats, top_words


def run_engine(input_file, mode, threads=4):
    """
    Run the C++ CorpusLens engine.
    """

    try:

        if mode == "Sequential":

            command = [
                str(SEQUENTIAL),
                str(input_file)
            ]

        else:

            command = [
                str(PARALLEL),
                str(input_file),
                str(threads)
            ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=str(ROOT)
        )

        if result.returncode != 0:

            return (
                "ERROR:\n\n"
                + result.stderr
                + "\n\n"
                + result.stdout
            )

        return result.stdout

    except Exception as error:

        return f"ERROR: {error}"


def save_uploaded_file(uploaded_file):
    """
    Save uploaded Streamlit file to a temporary file.
    """

    suffix = Path(uploaded_file.name).suffix

    if suffix == "":
        suffix = ".txt"

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    )

    temp_file.write(uploaded_file.getbuffer())
    temp_file.close()

    return Path(temp_file.name)


def benchmark_uploaded_file(input_file):
    """
    Benchmark the uploaded corpus using sequential and
    multiple parallel thread configurations.
    """

    results = []

    # --------------------------------------------------------
    # Sequential
    # --------------------------------------------------------

    sequential_output = run_engine(
        input_file,
        "Sequential"
    )

    sequential_stats, _ = parse_output(
        sequential_output
    )

    sequential_time = sequential_stats.get(
        "execution_time"
    )

    if sequential_time is not None:

        results.append(
            {
                "Mode": "Sequential",
                "Threads": 1,
                "Execution Time": sequential_time
            }
        )

    # --------------------------------------------------------
    # Parallel
    # --------------------------------------------------------

    for thread_count in [1, 2, 4, 8]:

        parallel_output = run_engine(
            input_file,
            "Parallel",
            thread_count
        )

        parallel_stats, _ = parse_output(
            parallel_output
        )

        parallel_time = parallel_stats.get(
            "execution_time"
        )

        if parallel_time is not None:

            results.append(
                {
                    "Mode": "Parallel",
                    "Threads": thread_count,
                    "Execution Time": parallel_time
                }
            )

    return pd.DataFrame(results)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Analysis Settings")

uploaded_file = st.sidebar.file_uploader(
    "Upload Corpus",
    type=["txt"]
)

mode = st.sidebar.radio(
    "Execution Mode",
    ["Parallel", "Sequential"],
    key="execution_mode_radio"
)

threads = 4

if mode == "Parallel":

    threads = st.sidebar.slider(
        "Number of Threads",
        min_value=1,
        max_value=16,
        value=4,
        step=1,
        key="analysis_threads_slider"
    )

run_analysis = st.sidebar.button(
    "▶ Run Analysis",
    type="primary",
    key="run_analysis_button"
)


# ============================================================
# MAIN ANALYSIS
# ============================================================

if uploaded_file is None:

    st.info(
        "👈 Upload a `.txt` corpus from the sidebar to begin."
    )

    st.markdown(
        """
        ### What CorpusLens analyzes

        - 📄 Total lines
        - 📑 Total paragraphs
        - 🔤 Total words
        - 📚 Unique words
        - 🔠 Total characters
        - ✏️ Total sentences
        - 📊 Average words per line
        - 📊 Average words per sentence
        - 📊 Average characters per line
        - 🔝 Most frequent words
        - ⚡ Sequential execution time
        - 🚀 Parallel execution time
        - 📈 Speedup
        - 📉 Parallel efficiency
        """
    )

else:

    st.success(
        f"Uploaded corpus: **{uploaded_file.name}**"
    )

    if run_analysis:

        temp_path = None

        try:

            # Save uploaded corpus
            temp_path = save_uploaded_file(
                uploaded_file
            )

            # ------------------------------------------------
            # RUN SELECTED ANALYSIS
            # ------------------------------------------------

            with st.spinner(
                "Running CorpusLens analysis..."
            ):

                output = run_engine(
                    temp_path,
                    mode,
                    threads
                )

            # Check engine error
            if output.startswith("ERROR"):

                st.error(
                    "The CorpusLens C++ engine returned an error."
                )

                st.code(
                    output,
                    language="text"
                )

            else:

                stats, top_words = parse_output(
                    output
                )

                # ------------------------------------------------
                # CORPUS STATISTICS
                # ------------------------------------------------

                st.header("📊 Corpus Statistics")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Total Lines",
                    f"{stats.get('total_lines', 0):,}"
                )

                col2.metric(
                    "Total Paragraphs",
                    f"{stats.get('total_paragraphs', 0):,}"
                )

                col3.metric(
                    "Total Words",
                    f"{stats.get('total_words', 0):,}"
                )

                col4.metric(
                    "Unique Words",
                    f"{stats.get('unique_words', 0):,}"
                )

                col5, col6, col7, col8 = st.columns(4)

                col5.metric(
                    "Characters",
                    f"{stats.get('total_characters', 0):,}"
                )

                col6.metric(
                    "Sentences",
                    f"{stats.get('total_sentences', 0):,}"
                )

                col7.metric(
                    "Words / Line",
                    f"{stats.get('avg_words_line', 0):.2f}"
                )

                col8.metric(
                    "Words / Sentence",
                    f"{stats.get('avg_words_sentence', 0):.2f}"
                )

                st.divider()

                # ------------------------------------------------
                # ADDITIONAL STATISTICS
                # ------------------------------------------------

                st.subheader("📐 Additional Statistics")

                additional_stats = pd.DataFrame(
                    {
                        "Metric": [
                            "Average words per line",
                            "Average words per sentence",
                            "Average characters per line"
                        ],
                        "Value": [
                            stats.get(
                                "avg_words_line",
                                0
                            ),
                            stats.get(
                                "avg_words_sentence",
                                0
                            ),
                            stats.get(
                                "avg_characters_line",
                                0
                            )
                        ]
                    }
                )

                st.dataframe(
                    additional_stats,
                    use_container_width=True,
                    hide_index=True
                )

                # ------------------------------------------------
                # TOP WORDS
                # ------------------------------------------------

                st.header("🔝 Top Frequent Words")

                if top_words:

                    top_df = pd.DataFrame(
                        top_words
                    )

                    left, right = st.columns(
                        [1, 1]
                    )

                    with left:

                        st.dataframe(
                            top_df,
                            use_container_width=True,
                            hide_index=True
                        )

                    with right:

                        chart_data = (
                            top_df
                            .set_index("Word")[
                                "Frequency"
                            ]
                        )

                        st.bar_chart(
                            chart_data
                        )

                else:

                    st.info(
                        "No top-word information was returned."
                    )

                st.divider()

                # ------------------------------------------------
                # EXECUTION RESULT
                # ------------------------------------------------

                st.header("⚡ Execution Result")

                execution_time = stats.get(
                    "execution_time"
                )

                if execution_time is not None:

                    if mode == "Parallel":

                        st.metric(
                            "Parallel Execution Time",
                            f"{execution_time:.6f} seconds"
                        )

                        st.metric(
                            "Threads Used",
                            stats.get(
                                "threads",
                                threads
                            )
                        )

                    else:

                        st.metric(
                            "Sequential Execution Time",
                            f"{execution_time:.6f} seconds"
                        )

                # ------------------------------------------------
                # RAW OUTPUT
                # ------------------------------------------------

                with st.expander(
                    "View Raw C++ Output"
                ):

                    st.code(
                        output,
                        language="text"
                    )

                # ====================================================
                # PERFORMANCE BENCHMARK
                # ====================================================

                st.divider()

                st.header(
                    "🚀 Performance Results for Uploaded Corpus"
                )

                st.write(
                    """
                    The uploaded corpus is executed using the
                    sequential implementation and multiple OpenMP
                    thread configurations.
                    """
                )

                with st.spinner(
                    "Benchmarking uploaded corpus..."
                ):

                    benchmark_df = benchmark_uploaded_file(
                        temp_path
                    )

                if benchmark_df.empty:

                    st.warning(
                        "No benchmark timing results were returned."
                    )

                else:

                    # ------------------------------------------------
                    # CLEAN DATA
                    # ------------------------------------------------

                    benchmark_df[
                        "Execution Time"
                    ] = pd.to_numeric(
                        benchmark_df[
                            "Execution Time"
                        ],
                        errors="coerce"
                    )

                    benchmark_df = benchmark_df.dropna(
                        subset=["Execution Time"]
                    )

                    # Remove invalid zero/negative measurements
                    # from speedup calculations.
                    valid_df = benchmark_df[
                        benchmark_df[
                            "Execution Time"
                        ] > 0
                    ].copy()

                    if valid_df.empty:

                        st.warning(
                            """
                            The corpus is too small for reliable
                            timing measurements. The C++ program is
                            reporting execution times as 0 seconds.

                            Try a larger corpus such as:
                            `data/corpus_5MB.txt`
                            or
                            `data/corpus_50MB.txt`.
                            """
                        )

                        st.dataframe(
                            benchmark_df,
                            use_container_width=True,
                            hide_index=True
                        )

                    else:

                        # ------------------------------------------------
                        # SEQUENTIAL BASELINE
                        # ------------------------------------------------

                        sequential_rows = valid_df[
                            valid_df["Mode"] == "Sequential"
                        ]

                        if sequential_rows.empty:

                            st.warning(
                                "Sequential baseline was not available."
                            )

                        else:

                            sequential_time = (
                                sequential_rows.iloc[0][
                                    "Execution Time"
                                ]
                            )

                            parallel_df = valid_df[
                                valid_df["Mode"] == "Parallel"
                            ].copy()

                            if parallel_df.empty:

                                st.warning(
                                    "No parallel benchmark results available."
                                )

                            else:

                                # ------------------------------------------------
                                # SPEEDUP
                                # ------------------------------------------------

                                parallel_df[
                                    "Speedup"
                                ] = (
                                    sequential_time
                                    / parallel_df[
                                        "Execution Time"
                                    ]
                                )

                                # ------------------------------------------------
                                # EFFICIENCY
                                # ------------------------------------------------

                                parallel_df[
                                    "Efficiency (%)"
                                ] = (
                                    parallel_df["Speedup"]
                                    / parallel_df["Threads"]
                                    * 100
                                )

                                # ------------------------------------------------
                                # FASTEST RESULT
                                # ------------------------------------------------

                                fastest_index = (
                                    parallel_df[
                                        "Execution Time"
                                    ].idxmin()
                                )

                                fastest_row = (
                                    parallel_df.loc[
                                        fastest_index
                                    ]
                                )

                                fastest_time = (
                                    fastest_row[
                                        "Execution Time"
                                    ]
                                )

                                fastest_threads = int(
                                    fastest_row[
                                        "Threads"
                                    ]
                                )

                                fastest_speedup = (
                                    fastest_row[
                                        "Speedup"
                                    ]
                                )

                                # ------------------------------------------------
                                # PERFORMANCE SUMMARY
                                # ------------------------------------------------

                                st.subheader(
                                    "🏁 Performance Summary"
                                )

                                p1, p2, p3, p4 = st.columns(4)

                                p1.metric(
                                    "Sequential Time",
                                    f"{sequential_time:.6f} s"
                                )

                                p2.metric(
                                    "Fastest Parallel Time",
                                    f"{fastest_time:.6f} s"
                                )

                                p3.metric(
                                    "Threads",
                                    fastest_threads
                                )

                                p4.metric(
                                    "Speedup",
                                    f"{fastest_speedup:.2f}×"
                                )

                                # ------------------------------------------------
                                # EXECUTION TIME TABLE
                                # ------------------------------------------------

                                st.subheader(
                                    "⏱ Execution Times"
                                )

                                display_df = valid_df.copy()

                                display_df[
                                    "Execution Time"
                                ] = display_df[
                                    "Execution Time"
                                ].map(
                                    lambda x: f"{x:.6f} s"
                                )

                                st.dataframe(
                                    display_df,
                                    use_container_width=True,
                                    hide_index=True
                                )

                                # ------------------------------------------------
                                # EXECUTION TIME GRAPH
                                # ------------------------------------------------

                                st.subheader(
                                    "📉 Execution Time vs Threads"
                                )

                                time_chart = (
                                    parallel_df[
                                        [
                                            "Threads",
                                            "Execution Time"
                                        ]
                                    ]
                                    .sort_values("Threads")
                                    .set_index("Threads")
                                )

                                st.line_chart(
                                    time_chart
                                )

                                # ------------------------------------------------
                                # SPEEDUP GRAPH
                                # ------------------------------------------------

                                st.subheader(
                                    "📈 Speedup vs Threads"
                                )

                                speedup_chart = (
                                    parallel_df[
                                        [
                                            "Threads",
                                            "Speedup"
                                        ]
                                    ]
                                    .sort_values("Threads")
                                    .set_index("Threads")
                                )

                                st.line_chart(
                                    speedup_chart
                                )

                                # ------------------------------------------------
                                # EFFICIENCY GRAPH
                                # ------------------------------------------------

                                st.subheader(
                                    "📊 Parallel Efficiency vs Threads"
                                )

                                efficiency_chart = (
                                    parallel_df[
                                        [
                                            "Threads",
                                            "Efficiency (%)"
                                        ]
                                    ]
                                    .sort_values("Threads")
                                    .set_index("Threads")
                                )

                                st.line_chart(
                                    efficiency_chart
                                )

                                # ------------------------------------------------
                                # DETAILED METRICS
                                # ------------------------------------------------

                                st.subheader(
                                    "📋 Detailed Performance Metrics"
                                )

                                metrics_df = parallel_df[
                                    [
                                        "Threads",
                                        "Execution Time",
                                        "Speedup",
                                        "Efficiency (%)"
                                    ]
                                ].copy()

                                metrics_df[
                                    "Execution Time"
                                ] = metrics_df[
                                    "Execution Time"
                                ].round(6)

                                metrics_df[
                                    "Speedup"
                                ] = metrics_df[
                                    "Speedup"
                                ].round(3)

                                metrics_df[
                                    "Efficiency (%)"
                                ] = metrics_df[
                                    "Efficiency (%)"
                                ].round(2)

                                st.dataframe(
                                    metrics_df,
                                    use_container_width=True,
                                    hide_index=True
                                )

                                # ------------------------------------------------
                                # EXPLANATION
                                # ------------------------------------------------

                                st.subheader(
                                    "💡 Performance Interpretation"
                                )

                                st.markdown(
                                    f"""
                                    **Sequential execution:**
                                    `{sequential_time:.6f}` seconds

                                    **Fastest measured parallel execution:**
                                    `{fastest_time:.6f}` seconds using
                                    **{fastest_threads} threads**

                                    **Measured speedup:**
                                    `{fastest_speedup:.2f}×`

                                    Speedup is calculated as:

                                    `Speedup = Sequential Time / Parallel Time`

                                    Parallel efficiency is calculated as:

                                    `Efficiency = Speedup / Number of Threads × 100`

                                    These measurements show how execution
                                    time changes as the number of OpenMP
                                    threads increases.
                                    """
                                )

        finally:

            # Remove temporary uploaded file
            if temp_path is not None:

                try:
                    os.unlink(temp_path)
                except Exception:
                    pass


# ============================================================
# EXISTING BENCHMARK PLOTS
# ============================================================

st.divider()

st.header("📊 Existing Benchmark Results")

st.write(
    """
    These graphs are generated from the benchmark datasets
    already stored in the CorpusLens `results/plots` directory.
    """
)

if PLOTS.exists():

    plot_files = sorted(
        PLOTS.glob("*.png")
    )

    if plot_files:

        selected_plot = st.selectbox(
            "Select an existing benchmark graph",
            [
                plot.name
                for plot in plot_files
            ],
            key="saved_plot_selector"
        )

        st.image(
            str(PLOTS / selected_plot),
            use_container_width=True
        )

    else:

        st.info(
            "No saved benchmark graphs were found."
        )

else:

    st.info(
        "The results/plots directory does not exist yet."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CorpusLens — C++ text analysis with OpenMP parallel processing"
)