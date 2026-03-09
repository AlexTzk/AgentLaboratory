"""
Configuration Guide for API Base URLs

Note: You can set `OLLAMA_API_BASE_URL` to your Ollama API URL if you are using it.
      You still need to set the `api_key` to the `ollama` when using it. (The `OpenAI API Key` field in the UI)
      Because we use it to identify if we are using ollama providers
      Then you can set any model string in the `args.llm_backend` flag or the `Custom LLM Backend (For Ollama)` field in the UI.

Read more about Ollama: https://ollama.com/blog/openai-compatibility
"""
GOOGLE_GENERATIVE_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/"
DEEPSEEK_API_BASE_URL = "https://api.deepseek.com/v1"
OLLAMA_API_BASE_URL = "http://localhost:11434/v1/"

"""
TASK_NOTE_LLM Configuration Guide

# Phase Configuration
- phases need to one of the following: 
- ["literature review", "plan formulation", 
   "data preparation", "running experiments", 
   "results interpretation", "report writing", 
   "report refinement"]

--- 
# Note Configuration
There are some variables that you can use in the note, you can use them by putting them in double curly braces.
Example: "You should write the report in {{language}}"

Here are the available variables for common use:
- research_topic: The research topic of the task
- api_key: OpenAI API Key
- deepseek_api_key: Deepseek API Key
- google_api_key: Google API Key
- anthropic_api_key: Anthropic API Key
- language: The language to use for the report
- llm_backend: The backend to use for the LLM
"""

"""
Configuration Guide for API Base URLs

Note: Set OLLAMA_API_BASE_URL to your Ollama API URL if using it.
      Set api_key to 'ollama' in the UI when using Ollama.
"""
GOOGLE_GENERATIVE_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/"
DEEPSEEK_API_BASE_URL          = "https://api.deepseek.com/v1"
OLLAMA_API_BASE_URL            = "http://localhost:11434/v1/"


"""
TASK_NOTE_LLM Configuration
Available template variables: {{research_topic}}, {{language}}, {{api_key}},
{{deepseek_api_key}}, {{google_api_key}}, {{anthropic_api_key}}, {{llm_backend}}
"""
TASK_NOTE_LLM = [

    # ── Plan Formulation ──────────────────────────────────────────────────────
    {
        "phases": ["literature review"],
        "note": (
            "Find 3–5 relevant papers and move on. Focus on:\n"
            "  1. Sparse InSAR reconstruction (e.g. kriging-based sensor placement)\n"
            "  2. Jump/change-point detection in deformation time series\n"
            "  3. Tweedie or zero-inflated models for geophysical increments\n\n"
        )
    },
    {
        "phases": ["plan formulation"],
        "note": (
            "Design a plan for exactly TWO experiments for ground motion / subsidence detection "
            "using EGMS Level 3 InSAR data:\n\n"
            "1. SAMPLE SIZE: Use at least 10,000 uniformly sampled points from the full dataset "
            "(~139K).\n\n"
            "2. JUMP THRESHOLD: Define the jump threshold ONCE and use it consistently throughout. "
            "Choose either: (a) a physically motivated fixed threshold (e.g. 6 mm), OR "
            "(b) a data-driven threshold (e.g. training-set 95th percentile). "
            "Do not mix them between sections. Report the numeric value obtained.\n\n"
            "3. TEST SET SIZE: Ensure at least 10 held-out test epochs for Experiment 2. "
            "A 70/30 chronological split on a 44-epoch series yields only ~13 epochs — use all of "
            "them. Do not further reduce the test window.\n\n"
            "4. BASELINES: Include at least two named baselines for jump detection: "
            "(a) a simple velocity-threshold alarm rule, and "
            "(b) a dense uniform sampling strategy (all points). "
            "All precision/recall metrics must be reported relative to these baselines.\n\n"
            "You have access to a local dataset, file structure and names below:\n\n"
            "The dataset is EGMS (European Ground Motion Service) Level 3 Ortho product "
            "for 100×100 km tile E32N34. Folder layout:\n\n"
            "  EGMS_L3_E32N34_100km_E_2018_2022_1/  ← East-West displacement, 2018–2022\n"
            "  EGMS_L3_E32N34_100km_U_2018_2022_1/  ← Vertical (Up) displacement, 2018–2022\n"
            "  EGMS_L3_E32N34_100km_U_2019_2023_1/  ← Vertical (Up) displacement, 2019–2023\n\n"
            "Each folder contains three file types:\n"
            "  .csv  → Point measurement table. Key columns: pid, latitude, longitude, "
            "mean_velocity (mm/year), rmse_ts (mm), acceleration (mm/yr²), "
            "plus dated displacement time-series columns (one per SAR acquisition).\n"
            "  .tiff → GeoTIFF raster of mean velocity. Read with rasterio. "
            "CRS is EPSG:4326 (geographic). NoData = -9999.\n"
            "  .xml  → Product metadata: sensor (Sentinel-1), temporal range, CRS, "
            "GNSS calibration info.\n\n"
        )
    },

    # ── Data Preparation ─────────────────────────────────────────────────────
    {
        "phases": ["data preparation"],
        "note": (
            "Design a plan for exactly TWO experiments for ground motion / subsidence detection "
            "using EGMS Level 3 InSAR data:\n\n"
            "1. SAMPLE SIZE: Use at least 10,000 uniformly sampled points from the full dataset "
            "(~139K).\n\n"
            "2. JUMP THRESHOLD: Define the jump threshold ONCE and use it consistently throughout. "
            "Choose either: (a) a physically motivated fixed threshold (e.g. 6 mm), OR "
            "(b) a data-driven threshold (e.g. training-set 95th percentile). "
            "Do not mix them between sections. Report the numeric value obtained.\n\n"
            "3. TEST SET SIZE: Ensure at least 10 held-out test epochs for Experiment 2. "
            "A 70/30 chronological split on a 44-epoch series yields only ~13 epochs — use all of "
            "them. Do not further reduce the test window.\n\n"
            "4. BASELINES: Include at least two named baselines for jump detection: "
            "(a) a simple velocity-threshold alarm rule, and "
            "(b) a dense uniform sampling strategy (all points). "
            "All precision/recall metrics must be reported relative to these baselines.\n\n"
            "You have access to a local dataset, file structure and names below:\n\n"
            "The dataset is EGMS (European Ground Motion Service) Level 3 Ortho product "
            "for 100×100 km tile E32N34. Folder layout:\n\n"
            "  EGMS_L3_E32N34_100km_E_2018_2022_1/  ← East-West displacement, 2018–2022\n"
            "  EGMS_L3_E32N34_100km_U_2018_2022_1/  ← Vertical (Up) displacement, 2018–2022\n"
            "  EGMS_L3_E32N34_100km_U_2019_2023_1/  ← Vertical (Up) displacement, 2019–2023\n\n"
            "Each folder contains three file types:\n"
            "  .csv  → Point measurement table. Key columns: pid, latitude, longitude, "
            "mean_velocity (mm/year), rmse_ts (mm), acceleration (mm/yr²), "
            "plus dated displacement time-series columns (one per SAR acquisition).\n"
            "  .tiff → GeoTIFF raster of mean velocity. Read with rasterio. "
            "CRS is EPSG:4326 (geographic). NoData = -9999.\n"
            "  .xml  → Product metadata: sensor (Sentinel-1), temporal range, CRS, "
            "GNSS calibration info.\n\n"
        )
    },

    # ── Running Experiments ──────────────────────────────────────────────────
    {
        "phases": ["running experiments"],
        "note": (
            "Time-series decomposition: use scipy.signal or statsmodels.\n\n"
            "When cross-matching the two temporal datasets spatially, use a nearest-neighbour "
            "join with a max distance tolerance of 0.0001 degrees (~10 m). "
            "Always filter out points with rmse_ts > 2.0 mm before analysis "
            "(high residual = unreliable measurement)."
        )
    },

    # ── Hardware (Apple Silicon — MPS not CUDA) ──────────────────────────────
    {
        "phases": ["data preparation", "running experiments"],
        "note": (
            "You are running on a Mac M3 Max with 128 GB of RAM. "
            "For PyTorch GPU acceleration use Apple Metal (MPS), NOT cuda:\n\n"
            "  device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')\n\n"
            "Do NOT use device='cuda' — it will silently fall back to CPU on this machine."
        )
    },

    # ── Visualization ────────────────────────────────────────────────────────
    {
        "phases": ["data preparation", "running experiments", "results interpretation"],
        "note": (
            "Produce colorful, publication-quality figures:\n"
            "  - Spatial velocity maps: diverging colormap 'RdBu_r' or 'coolwarm' centered at 0, "
            "colorbar (mm/year), lat/lon gridlines, north arrow, scale bar.\n"
            "  - Time-series plots: multi-line, one line per cluster/hotspot, "
            "shaded ±1σ confidence bands, vertical lines at season boundaries.\n"
            "  - Jump detection: include a precision-recall curve for each method on the same axes.\n"
            "  - Sampling efficiency (Exp 1): NRMSE vs N with stratified lines "
            "(low/medium/high velocity), error bars, and a dashed vertical line at N=25.\n"
            "  - Histograms: log-scale y-axis, dashed vertical line at subsidence threshold.\n\n"
            "IMPORTANT — figure paths: use RELATIVE paths only (e.g. 'figures/Figure_1.png'). "
            "Never hardcode absolute paths like '/Users/alex/...'. "
            "Save all figures as PNG at dpi=300 into the 'figures/' subdirectory."
        )
    },

    # ── Results Interpretation ───────────────────────────────────────────────
    {
        "phases": ["results interpretation"],
        "note": (
            "Contextualise subsidence patterns against known geophysical causes: "
            "groundwater extraction, mining activity, clay consolidation, salt dissolution, "
            "or anthropogenic loading (urban infrastructure).\n\n"
            "Cross-reference detected U-component hotspots with E-component data: "
            "if horizontal motion correlates spatially with vertical subsidence, "
            "consider slope instability or fault-related mechanisms rather than pure compaction.\n\n"
            "Report: mean velocity (mm/year), peak velocity, total cumulative displacement (mm) "
            "over the observation window, and estimated affected area (km²) for each hotspot. "
            "Note that EGMS L3 has a spatial resolution of ~100 m and a temporal baseline "
            "limited by Sentinel-1 revisit (6–12 days)."
        )
    },

    # ── Report Structure ─────────────────────────────────────────────────────
    {
        "phases": ["report writing", "report refinement"],
        "note": (
            "Structure the report as follows:\n"
            "  1. Abstract\n"
            "  2. Introduction — InSAR principles, EGMS programme background, subsidence significance\n"
            "  3. Study Area & Dataset — tile E32N34 context, data components (E/U), temporal coverage\n"
            "  4. Methodology — one subsection per experiment\n"
            "  5. Results — velocity maps, hotspot statistics table, temporal comparison plots\n"
            "  6. Discussion — subsidence mechanisms, EGMS L3 limitations (temporal decorrelation, "
            "atmospheric artefacts, point density), comparison to literature\n"
            "  7. Conclusion\n\n"
            "Include a summary table comparing Experiment 1 vs Experiment 2: "
            "hotspot count, mean/max velocity, affected area, data period."
        )
    },

    # ── Language (all phases) ────────────────────────────────────────────────
    {
        "phases": [
            "literature review", "plan formulation", "data preparation",
            "running experiments", "results interpretation",
            "report writing", "report refinement"
        ],
        "note": "Always converse and write the report in the following language: {{language}}"
    },
]


"""
Human-in-the-Loop Configuration
  True  → always human-supervised
  False → fully automated
  None  → inherits from args.copilot_mode / UI checkbox
"""
CONFIG_HUMAN_IN_THE_LOOP = {
    "literature review":      False,  # Automated broad InSAR/subsidence survey
    "plan formulation":       False,   # Review experiment design before committing
    "data preparation":       False,  # Well-defined pipeline, no supervision needed
    "running experiments":    False,  # Deterministic spatial/statistical analysis
    "results interpretation": False,   # Human validation of subsidence findings is critical
    "report writing":         False,  # Automated draft from structured template
    "report refinement":      False,   # Final review before output
}


"""
Agent Models Configuration
Assign stronger reasoning models to phases that require domain synthesis.
Set to None to inherit from args.llm_backend / UI selection.

CONFIG_AGENT_MODELS = {
    "literature review":      "deepseek-reasoner",  # Long-context synthesis of InSAR literature
    "plan formulation":       "deepseek-reasoner",  # Experimental design requires strong reasoning
    "data preparation":       None,                 # Mechanical pipeline — default model sufficient
    "running experiments":    None,                 # Code execution — default model sufficient
    "results interpretation": "deepseek-reasoner",  # Domain reasoning for geophysical interpretation
    "report writing":         "deepseek-chat",      # Fast, coherent long-form writing
    "report refinement":      "deepseek-chat",      # Quick iteration on draft sections
}"""

"""
CONFIG_HUMAN_IN_THE_LOOP = {
    "literature review":      None,
    "plan formulation":       None,
    "data preparation":       None,
    "running experiments":    None,
    "results interpretation": None,
    "report writing":         None,
    "report refinement":      None,
}"""

"""
Agent Models Configuration Guide

You can configure the LLM Backend used for the different phases.
- If the value is a string, the stage will use the specified backend.
- If the value is `None`, the stage will take the configuration from the `args.llm_backend` flag.
  (Or whatever model you select or set in the UI)
"""
CONFIG_AGENT_MODELS = {
    "literature review":      None,
    "plan formulation":       None,
    "data preparation":       None,
    "running experiments":    None,
    "results interpretation": None,
    "report writing":         None,
    "report refinement":      None,
}
