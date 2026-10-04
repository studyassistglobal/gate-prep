# Builds GATE note chapter modules from the Master_Guide markdown sources.
# MD -> typed block AST -> src/data/notes/de/chN.js  (GENERATED — do not hand-edit)
#
# Block types: p, h3, h4, ul, ol, table, code, alert, details, img, math
# The MD's own Table-of-Contents sections are dropped (the app generates its own).
import json, os, re, shutil, datetime

BASE = r"D:\UVM\PROJECTS\qp to test\gate-prep"
SRC_ROOT = r"D:\GATE 2027"

CHAPTERS = [
    {
        "id": "de-ch1",
        "file": "ch1",
        "notes_sub": "de",
        "num": 1,
        "title": "Logic Gates & Boolean Algebra",
        "subject": "Digital Electronics",
        "md": os.path.join(SRC_ROOT, "Digital electronics", "Chapter_01_Logic_Gates_and_Boolean_Algebra_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Digital electronics", "figures"),
        "figures_dst": "notes/de/figures",
        "fig_prefix": "figures/",
        "web_prefix": "/notes/de/figures/",
    },
    {
        "id": "de-ch2",
        "file": "ch2",
        "notes_sub": "de",
        "num": 2,
        "title": "Representation of Boolean Expressions & K-Maps",
        "subject": "Digital Electronics",
        "md": os.path.join(SRC_ROOT, "Digital electronics", "Chapter_02_Representation_of_Boolean_Expressions_and_K_Maps_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Digital electronics", "figures_ch2"),
        "figures_dst": "notes/de/figures_ch2",
        "fig_prefix": "figures_ch2/",
        "web_prefix": "/notes/de/figures_ch2/",
    },
    {
        "id": "de-ch3",
        "notes_sub": "de",
        "file": "ch3",
        "num": 3,
        "title": "Number Systems & Digital Representation",
        "subject": "Digital Electronics",
        "md": os.path.join(SRC_ROOT, "Digital electronics", "Chapter_03_Number_Systems_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Digital electronics", "figures_ch3"),
        "figures_dst": "notes/de/figures_ch3",
        "fig_prefix": "figures_ch3/",
        "web_prefix": "/notes/de/figures_ch3/",
    },
    {
        "id": "de-ch4-p1",
        "notes_sub": "de",
        "file": "ch4p1",
        "num": 4,
        "part": 1,
        "title": "Combinational Circuits — Arithmetic Logic",
        "subject": "Digital Electronics",
        "md": os.path.join(SRC_ROOT, "Digital electronics", "chapters", "Chapter_04_Part1_Combinational_Circuits.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/de/figures_ch4/",
    },
    {
        "id": "de-ch4-p2",
        "notes_sub": "de",
        "file": "ch4p2",
        "num": 4,
        "part": 2,
        "title": "Combinational Circuits — Advanced Architectures",
        "subject": "Digital Electronics",
        "md": os.path.join(SRC_ROOT, "Digital electronics", "chapters", "Chapter_04_Part2_Combinational_Circuits.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/de/figures_ch4/",
    },
    {
        "id": "ss-ch1",
        "file": "ssch1",
        "notes_sub": "ss",
        "num": 1,
        "title": "Basics of Signals",
        "subject": "Signals & Systems",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_01_Basics_of_Signals_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Signals and Systems", "figures_ch1"),
        "figures_dst": "notes/ss/figures_ch1",
        "fig_prefix": "figures_ch1/",
        "web_prefix": "/notes/ss/figures_ch1/",
    },
    {
        "id": "ss-ch2",
        "file": "ssch2",
        "notes_sub": "ss",
        "num": 2,
        "title": "Basics of Systems",
        "subject": "Signals & Systems",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_02_Basics_of_Systems_Master_Guide.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ss/",
    },
    {
        "id": "ssf-ch1",
        "file": "ssfch1",
        "notes_sub": "ssf",
        "num": 1,
        "title": "Basics of Signals — Formula & Revision Sheet",
        "subject": "Signals & Systems",
        "section_split": "section",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_01_Basics_of_Signals_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ss/",
    },
    {
        "id": "ssf-ch2",
        "file": "ssfch2",
        "notes_sub": "ssf",
        "num": 2,
        "title": "Basics of Systems — Formula & Revision Sheet",
        "subject": "Signals & Systems",
        "section_split": "section",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_02_Basics_of_Systems_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ss/",
    },
    {
        "id": "ssf-ch3",
        "file": "ssfch3",
        "notes_sub": "ssf",
        "num": 3,
        "title": "Fourier Series (CTFS) — Formula & Revision Sheet",
        "subject": "Signals & Systems",
        "section_split": "section",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_03_Continuous_Time_Fourier_Series_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ssf/",
    },
    {
        "id": "ss-ch3",
        "unwrap": True,
        "file": "ssch3",
        "notes_sub": "ss",
        "num": 3,
        "title": "Continuous-Time Fourier Series (CTFS)",
        "subject": "Signals & Systems",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_03_Continuous_Time_Fourier_Series_Master_Guide.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ss/",
    },
    {
        "id": "ss-ch4",
        "unwrap": True,
        "file": "ssch4",
        "notes_sub": "ss",
        "num": 4,
        "title": "Fourier Transform & Sampling Theorem",
        "subject": "Signals & Systems",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_04_Continuous_Time_Fourier_Transform_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Signals and Systems", "figures_ch4"),
        "figures_dst": "notes/ss/figures_ch4",
        "fig_prefix": "figures_ch4/",
        "web_prefix": "/notes/ss/figures_ch4/",
    },
    {
        "id": "ss-ch5",
        "unwrap": True,
        "file": "ssch5",
        "notes_sub": "ss",
        "num": 5,
        "title": "Continuous-Time Laplace Transform",
        "subject": "Signals & Systems",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_05_Continuous_Time_Laplace_Transform_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Signals and Systems", "figures_ch5"),
        "figures_dst": "notes/ss/figures_ch5",
        "fig_prefix": "figures_ch5/",
        "web_prefix": "/notes/ss/figures_ch5/",
    },
    {
        "id": "ss-ch6",
        "unwrap": True,
        "file": "ssch6",
        "notes_sub": "ss",
        "num": 6,
        "title": "Discrete-Time Z-Transform",
        "subject": "Signals & Systems",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_06_Discrete_Time_Z_Transform_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Signals and Systems", "figures_ch6"),
        "figures_dst": "notes/ss/figures_ch6",
        "fig_prefix": "figures_ch6/",
        "web_prefix": "/notes/ss/figures_ch6/",
    },
    {
        "id": "ss-ch7",
        "unwrap": True,
        "file": "ssch7",
        "notes_sub": "ss",
        "num": 7,
        "title": "DTFT, DTFS, DFT & FFT",
        "subject": "Signals & Systems",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_07_DTFT_DTFS_DFT_FFT_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Signals and Systems", "figures_ch7"),
        "figures_dst": "notes/ss/figures_ch7",
        "fig_prefix": "figures_ch7/",
        "web_prefix": "/notes/ss/figures_ch7/",
    },
    {
        "id": "ssf-ch4",
        "unwrap": True,
        "file": "ssfch4",
        "notes_sub": "ssf",
        "num": 4,
        "title": "Fourier Transform & Sampling — Formula & Revision Sheet",
        "subject": "Signals & Systems",
        "section_split": "section",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_04_Continuous_Time_Fourier_Transform_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ssf/",
    },
    {
        "id": "ssf-ch5",
        "unwrap": True,
        "file": "ssfch5",
        "notes_sub": "ssf",
        "num": 5,
        "title": "Laplace Transform — Formula & Revision Sheet",
        "subject": "Signals & Systems",
        "section_split": "section",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_05_Continuous_Time_Laplace_Transform_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ssf/",
    },
    {
        "id": "ssf-ch6",
        "unwrap": True,
        "file": "ssfch6",
        "notes_sub": "ssf",
        "num": 6,
        "title": "Z-Transform — Formula & Revision Sheet",
        "subject": "Signals & Systems",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_06_Discrete_Time_Z_Transform_Formula_and_Revision_Sheet.md"),
        "figures_src": os.path.join(SRC_ROOT, "Signals and Systems", "figures_ch6"),
        "figures_dst": "notes/ssf/figures_ch6",
        "fig_prefix": "figures_ch6/",
        "web_prefix": "/notes/ssf/figures_ch6/",
    },
    {
        "id": "ssf-ch7",
        "unwrap": True,
        "file": "ssfch7",
        "notes_sub": "ssf",
        "num": 7,
        "title": "DTFT, DTFS, DFT & FFT — Formula & Revision Sheet",
        "subject": "Signals & Systems",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_07_DTFT_DTFS_DFT_FFT_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ssf/",
    },
    {
        "id": "nt-ch1",
        "unwrap": True,
        "fig_links": True,
        "file": "nt1",
        "notes_sub": "nt",
        "num": 1,
        "title": "Basics of Network Analysis",
        "subject": "Network Theory",
        "section_split": "h1",
        "md": os.path.join(SRC_ROOT, "Network Theory", "Basics_of_Network_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Network Theory", "figures_network_basics"),
        "figures_dst": "notes/nt/figures_network_basics",
        "fig_prefix": "figures_network_basics/",
        "web_prefix": "/notes/nt/figures_network_basics/",
    },
    {
        "id": "nt-ch2",
        "unwrap": True,
        "fig_links": True,
        "file": "nt2",
        "notes_sub": "nt",
        "num": 2,
        "title": "Network Theorems & Circuit Equivalence",
        "subject": "Network Theory",
        "section_split": "h1",
        "md": os.path.join(SRC_ROOT, "Network Theory", "Network_Theorems_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Network Theory", "figures_network_theorems"),
        "figures_dst": "notes/nt/figures_network_theorems",
        "fig_prefix": "figures_network_theorems/",
        "web_prefix": "/notes/nt/figures_network_theorems/",
    },
    {
        "id": "nt-ch3",
        "unwrap": True,
        "fig_links": True,
        "file": "nt3",
        "notes_sub": "nt",
        "num": 3,
        "title": "Transient Analysis",
        "subject": "Network Theory",
        "section_split": "h1",
        "md": os.path.join(SRC_ROOT, "Network Theory", "Transient_Analysis_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Network Theory", "figures_transient_analysis"),
        "figures_dst": "notes/nt/figures_transient_analysis",
        "fig_prefix": "figures_transient_analysis/",
        "web_prefix": "/notes/nt/figures_transient_analysis/",
    },
    {
        "id": "ntf-ch1",
        "unwrap": True,
        "fig_links": True,
        "file": "ntf1",
        "notes_sub": "ntf",
        "num": 1,
        "title": "Basics of Network — Formula & Revision Sheet",
        "subject": "Network Theory",
        "md": os.path.join(SRC_ROOT, "Network Theory", "Basics_of_Network_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_ref": os.path.join(SRC_ROOT, "Network Theory", "figures_network_basics"),
        "figures_dst": None,
        "fig_prefix": "figures_network_basics/",
        "web_prefix": "/notes/nt/figures_network_basics/",
    },
    {
        "id": "ntf-ch2",
        "unwrap": True,
        "fig_links": True,
        "file": "ntf2",
        "notes_sub": "ntf",
        "num": 2,
        "title": "Network Theorems — Formula & Revision Sheet",
        "subject": "Network Theory",
        "md": os.path.join(SRC_ROOT, "Network Theory", "Network_Theorems_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ntf/",
    },
    {
        "id": "ntf-ch3",
        "unwrap": True,
        "fig_links": True,
        "file": "ntf3",
        "notes_sub": "ntf",
        "num": 3,
        "title": "Transient Analysis — Formula & Revision Sheet",
        "subject": "Network Theory",
        "md": os.path.join(SRC_ROOT, "Network Theory", "Transient_Analysis_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_ref": os.path.join(SRC_ROOT, "Network Theory", "figures_transient_analysis"),
        "figures_dst": None,
        "fig_prefix": "figures_transient_analysis/",
        "web_prefix": "/notes/nt/figures_transient_analysis/",
    },
    {
        "id": "em-ch1",
        "unwrap": True,
        "file": "emch1",
        "notes_sub": "em",
        "num": 1,
        "title": "Linear Algebra",
        "subject": "Engineering Mathematics",
        "section_split": "part",
        "md": os.path.join(SRC_ROOT, "engineering mathematics", "Engineering_Mathematics_Linear_Algebra_Master_Guide.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/em/",
    },
    {
        "id": "emf-ch1",
        "unwrap": True,
        "file": "emfch1",
        "notes_sub": "emf",
        "num": 1,
        "title": "Linear Algebra — Formula & Revision Sheet",
        "subject": "Engineering Mathematics",
        "md": os.path.join(SRC_ROOT, "engineering mathematics", "Engineering_Mathematics_Linear_Algebra_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/emf/",
    },
    {
        "id": "edc-ch1",
        "unwrap": True,
        "file": "edcch1",
        "notes_sub": "edc",
        "num": 1,
        "title": "Electronic Devices & Circuits (EDC)",
        "subject": "Electronic Devices & Circuits",
        "section_split": "part",
        "md": os.path.join(SRC_ROOT, "edc", "Engineering_Electronics_EDC_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "edc", "figures_edc"),
        "figures_dst": "notes/edc/figures_edc",
        "fig_prefix": "figures_edc/",
        "web_prefix": "/notes/edc/figures_edc/",
    },
    {
        "id": "edcf-ch1",
        "unwrap": True,
        "file": "edcfch1",
        "notes_sub": "edcf",
        "num": 1,
        "title": "EDC — Formula & Revision Sheet",
        "subject": "Electronic Devices & Circuits",
        "md": os.path.join(SRC_ROOT, "edc", "Engineering_Electronics_EDC_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/edcf/",
    },
    {
        "id": "ae-ch1",
        "unwrap": True,
        "fig_links": True,
        "file": "ae1",
        "notes_sub": "ae",
        "num": 1,
        "title": "Diode Circuits, Rectifiers & Filters",
        "subject": "Analog Electronics",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "analog electronics", "Analog_Electronics_Diode_Circuits_and_Rectifiers_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "analog electronics", "figures_analog_electronics"),
        "figures_dst": "notes/ae/figures_analog_electronics",
        "fig_prefix": "figures_analog_electronics/",
        "web_prefix": "/notes/ae/figures_analog_electronics/",
    },
    {
        "id": "aef-ch1",
        "unwrap": True,
        "fig_links": True,
        "file": "aef1",
        "notes_sub": "aef",
        "num": 1,
        "title": "Diode Circuits & Rectifiers — Formula & Revision Sheet",
        "subject": "Analog Electronics",
        "md": os.path.join(SRC_ROOT, "analog electronics", "Analog_Electronics_Diode_Circuits_and_Rectifiers_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_ref": os.path.join(SRC_ROOT, "analog electronics", "figures_analog_electronics"),
        "figures_dst": None,
        "fig_prefix": "figures_analog_electronics/",
        "web_prefix": "/notes/ae/figures_analog_electronics/",
    },
    {
        "id": "em-ch2",
        "unwrap": True,
        "file": "emch2",
        "notes_sub": "em",
        "num": 2,
        "title": "Calculus",
        "subject": "Engineering Mathematics",
        "section_split": "part",
        "md": os.path.join(SRC_ROOT, "engineering mathematics", "Engineering_Mathematics_Calculus_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "engineering mathematics", "figures_calculus"),
        "figures_dst": "notes/em/figures_calculus",
        "fig_prefix": "figures_calculus/",
        "web_prefix": "/notes/em/figures_calculus/",
    },
    {
        "id": "em-ch3",
        "unwrap": True,
        "file": "emch3",
        "notes_sub": "em",
        "num": 3,
        "title": "Vector Calculus",
        "subject": "Engineering Mathematics",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "engineering mathematics", "Engineering_Mathematics_Vector_Calculus_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "engineering mathematics", "figures_vector_calculus"),
        "figures_dst": "notes/em/figures_vector_calculus",
        "fig_prefix": "figures_vector_calculus/",
        "web_prefix": "/notes/em/figures_vector_calculus/",
    },
    {
        "id": "em-ch4",
        "unwrap": True,
        "file": "emch4",
        "notes_sub": "em",
        "num": 4,
        "title": "Complex Analysis",
        "subject": "Engineering Mathematics",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "engineering mathematics", "Engineering_Mathematics_Complex_Analysis_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "engineering mathematics", "figures_complex_analysis"),
        "figures_dst": "notes/em/figures_complex_analysis",
        "fig_prefix": "figures_complex_analysis/",
        "web_prefix": "/notes/em/figures_complex_analysis/",
    },
    {
        "id": "em-ch5",
        "unwrap": True,
        "file": "emch5",
        "notes_sub": "em",
        "num": 5,
        "title": "Differential Equations",
        "subject": "Engineering Mathematics",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "engineering mathematics", "Engineering_Mathematics_Differential_Equations_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "engineering mathematics", "figures_differential_equations"),
        "figures_dst": "notes/em/figures_differential_equations",
        "fig_prefix": "figures_differential_equations/",
        "web_prefix": "/notes/em/figures_differential_equations/",
    },
    {
        "id": "em-ch6",
        "unwrap": True,
        "file": "emch6",
        "notes_sub": "em",
        "num": 6,
        "title": "Probability, Random Variables & Statistics",
        "subject": "Engineering Mathematics",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "engineering mathematics", "Engineering_Mathematics_Probability_and_Statistics_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "engineering mathematics", "figures_probability"),
        "figures_dst": "notes/em/figures_probability",
        "fig_prefix": "figures_probability/",
        "web_prefix": "/notes/em/figures_probability/",
    },
    {
        "id": "emf-ch2",
        "unwrap": True,
        "file": "emfch2",
        "notes_sub": "emf",
        "num": 2,
        "title": "Calculus — Formula & Revision Sheet",
        "subject": "Engineering Mathematics",
        "section_split": "section",
        "md": os.path.join(SRC_ROOT, "engineering mathematics", "Engineering_Mathematics_Calculus_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/emf/",
    },
    {
        "id": "emf-ch3",
        "unwrap": True,
        "file": "emfch3",
        "notes_sub": "emf",
        "num": 3,
        "title": "Vector Calculus — Formula & Revision Sheet",
        "subject": "Engineering Mathematics",
        "md": os.path.join(SRC_ROOT, "engineering mathematics", "Engineering_Mathematics_Vector_Calculus_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/emf/",
    },
    {
        "id": "emf-ch4",
        "unwrap": True,
        "file": "emfch4",
        "notes_sub": "emf",
        "num": 4,
        "title": "Complex Analysis — Formula & Revision Sheet",
        "subject": "Engineering Mathematics",
        "md": os.path.join(SRC_ROOT, "engineering mathematics", "Engineering_Mathematics_Complex_Analysis_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/emf/",
    },
    {
        "id": "emf-ch5",
        "unwrap": True,
        "file": "emfch5",
        "notes_sub": "emf",
        "num": 5,
        "title": "Differential Equations — Formula & Revision Sheet",
        "subject": "Engineering Mathematics",
        "md": os.path.join(SRC_ROOT, "engineering mathematics", "Engineering_Mathematics_Differential_Equations_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/emf/",
    },
    {
        "id": "emf-ch6",
        "unwrap": True,
        "file": "emfch6",
        "notes_sub": "emf",
        "num": 6,
        "title": "Probability & Statistics — Formula & Revision Sheet",
        "subject": "Engineering Mathematics",
        "md": os.path.join(SRC_ROOT, "engineering mathematics", "Engineering_Mathematics_Probability_and_Statistics_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/emf/",
    },
]

# Exact-match typo repairs applied to the (read-only) sources before parsing.
# Keys are chapter ids; values are (bad, good) literal replacements.
REPAIRS = {
    "nt-ch1": [
        ("the entire $2\\text{ mA} flows through branch BD",
         "the entire $2\\text{ mA}$ flows through branch BD"),
    ],
    # ss-ch5's source truncates module 09 mid-sentence (dangling "5. **The")
    "ss-ch5": [
        ("5. **The \n---", "---"),
    ],
    # em-ch1 drill: missing opening $ before \vert A \vert
    "em-ch1": [
        ("Since \\vert A \\vert \\neq 0$, the", "Since $\\vert A \\vert \\neq 0$, the"),
    ],
}


def slugify(title):
    t = re.sub(r"\$[^$]*\$", " ", title)          # strip inline math for stable slugs
    t = re.sub(r"<[^>]+>", " ", t)
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return re.sub(r"-{2,}", "-", t)


MATH_SPAN_RE = re.compile(r"\$([^$]+)\$")
PLAIN_MATH_RE = re.compile(r"^[^\\\{\}<>]+$")


def clean_title(title):
    """Section/module titles render as plain text (TOC sidebar, search, header),
    so $math$ cannot stay: keep the inner text when it is plain-readable
    (`$R$` -> R), otherwise drop the span, then tidy leftover punctuation."""
    def sub(m):
        inner = m.group(1).strip()
        return inner if PLAIN_MATH_RE.match(inner) else ""
    t = MATH_SPAN_RE.sub(sub, title)
    t = re.sub(r"\(\s*\)", " ", t)              # parens emptied by dropped spans
    t = re.sub(r"\s+(-)(?=[A-Za-z])", r"\1", t)  # "the -Plane" -> "the-Plane"
    t = re.sub(r"\s{2,}", " ", t).strip(" -,")
    return t or title.strip()


def rewrite_img_src(src, ch):
    """Map a source image reference onto the deployed figures URL. When a
    vector `.svg` twin exists for a raster reference it is preferred — the
    blueprints stay crisp at any zoom and are ~25x smaller than the JPGs."""
    if src.startswith("http"):
        return src
    twins = ch.get("_fig_files")
    if twins and re.search(r"\.(jpe?g|png)$", src, re.I):
        svg = re.sub(r"\.(jpe?g|png)$", ".svg", src, flags=re.I)
        if os.path.basename(svg) in twins:
            src = svg
    if ch["fig_prefix"] and src.startswith(ch["fig_prefix"]):
        return ch["web_prefix"] + src[len(ch["fig_prefix"]):]
    return ch["web_prefix"] + os.path.basename(src)


IMG_RE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$")

STRUCT_START = re.compile(r"^\s*(?:#{1,6}\s|>|[-*]\s|\d+[.)]\s|```|~~~|\$\$|\||<|!\[)")

# gallery figure links: the 4K blueprint galleries in the Network Theory /
# Analog Electronics sources reference figures as `[text](file:///...)` or
# `[text](figures_.../x.svg)` links — dead on the site. They are rewritten
# into standalone `![caption](target)` figure blocks (see convert_fig_links).
FIG_LINK = re.compile(r"\[([^\]]*)\]\(([^()\s]+?\.(?:jpg|jpeg|png|svg))\)", re.I)
SEP_ROW = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)$")


def fig_block(caption, url, scope=""):
    res = [f"![{caption}]({url})", ""]
    if scope.strip():
        res.extend([f"*Covers {scope.strip()}*", ""])
    return res


def gallery_table_to_figures(group):
    """One figure block per linked row; the header/separator and any unlinked
    rows are dropped — the captions carry the figure identity. The title comes
    from a fully-bold cell when the gallery keeps it separate (4-col variant)
    and falls back to the link text (sheet variant)."""
    res = []
    for row in group:
        if SEP_ROW.match(row):
            continue
        m = FIG_LINK.search(row)
        if not m:
            continue
        num, title, scope = "", "", []
        for c in split_table_row(row):
            cs = c.strip()
            if m.group(0) in c:
                continue
            if not num and re.fullmatch(r"\*{0,2}\d{1,2}\*{0,2}", cs):
                num = cs.strip("*")
                continue
            if not title and re.fullmatch(r"\*\*.+\*\*", cs):
                title = cs.strip("*").strip()
                continue
            if cs:
                scope.append(cs)
        if not title:
            title = re.sub(r"\*+", "", m.group(1)).strip()
        caption = f"Fig {num} — {title}" if num else title
        res.extend(fig_block(caption, m.group(2), " ".join(scope)))
    return res


def list_item_to_figure(body):
    m = FIG_LINK.search(body)
    pre = re.sub(r"\*+", "", body[: m.start()]).strip().rstrip(":").strip()
    title = re.sub(r"\*+", "", m.group(1)).strip()
    caption = " — ".join(p for p in (pre, title) if p) or title or "Figure"
    return fig_block(caption, m.group(2))


def convert_fig_links(raw):
    lines = raw.split("\n")
    out = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        # dead local-viewer links (`file:///....html`) -> plain text
        line = re.sub(r"\[([^\]]+)\]\(file:///[^)]*\.html?\)", r"\1", line)
        if re.match(r"^\s*\|.*\|\s*$", line):
            j = i
            group = []
            while j < n and re.match(r"^\s*\|.*\|\s*$", lines[j]):
                group.append(lines[j])
                j += 1
            if any(FIG_LINK.search(g) for g in group):
                out.extend(gallery_table_to_figures(group))
            else:
                out.extend(group)
            i = j
            continue
        m = LIST_ITEM.match(line)
        if m:
            body = m.group(1)
            if FIG_LINK.search(body) and not body.strip().startswith("!["):
                out.extend(list_item_to_figure(body))
                i += 1
                continue
        fm = FIG_LINK.search(line)
        if fm and re.fullmatch(r"\s*\[([^\]]*)\]\([^)]+\)\s*", line):
            out.extend(fig_block(re.sub(r"\*+", "", fm.group(1)).strip(), fm.group(2)))
            i += 1
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def unwrap_lines(lines):
    """Repair hard-wrapped lines (the Ch4-7 Masters and Network Theory sources
    wrap headings, bold spans and inline math mid-token). A continuation line
    is joined into its parent ONLY when the parent is actually broken: an
    unclosed bold (** count odd), an unclosed inline $...$ (odd $ count not
    from $$), a heading whose math/bold is broken, or a table row continued on
    a plain line. Healthy headings are never joined (module headers carry
    indented scope lines that must stay separate). Fenced code is untouched."""
    out = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        prev = out[-1] if out else None
        if (not in_fence and prev is not None and prev.strip() and line.strip()
                and not STRUCT_START.match(line)):
            ps = prev.rstrip()
            odd_dollar = (ps.count("$") - 2 * ps.count("$$")) % 2 == 1
            broken_bold = ps.count("**") % 2 == 1
            broken_heading = re.match(r"^\s*#{1,6}\s", ps) and (odd_dollar or broken_bold)
            if broken_heading or (broken_bold and not re.match(r"^\s*#{1,6}\s", ps)) \
                    or (odd_dollar and not re.match(r"^\s*#{1,6}\s", ps)) \
                    or ps.lstrip().startswith("|"):
                out[-1] = ps + " " + line.strip()
                continue
        out.append(line)
    return out


def split_table_row(line):
    """Split a pipe-table row into cells, ignoring `|` inside $math$/$$math$$,
    escaped \\|, or `backtick code spans`."""
    s = line.strip().strip("|")
    # stray trailing `\vert` separators (OCR of a dangling pipe) create a
    # phantom empty last cell — strip them
    s = re.sub(r"(?:\s*\\vert\s*)+$", "", s)
    cells, cur, in_math, in_code = [], [], False, False
    i = 0
    while i < len(s):
        ch = s[i]
        # OCR artifact: `\vert` used as a cell separator outside math
        if s.startswith("\\vert", i) and not in_math and not in_code:
            cells.append("".join(cur).strip())
            cur = []
            i += 5
            continue
        if ch == "\\" and i + 1 < len(s):
            cur.append(ch)
            cur.append(s[i + 1])
            i += 2
            continue
        if ch == "`" and not in_math:
            in_code = not in_code
            cur.append(ch)
            i += 1
            continue
        if s.startswith("$$", i):
            in_math = not in_math
            cur.append("$$")
            i += 2
            continue
        if ch == "$":
            in_math = not in_math
            cur.append(ch)
            i += 1
            continue
        if ch == "|" and not in_math and not in_code:
            cells.append("".join(cur).strip())
            cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    cells.append("".join(cur).strip())
    return cells

def inline_clean(text, ch):
    """Rewrite image links inside inline text (kept for p/ul/table cells) and
    strip stray <details>/<summary> tags the sources mention in prose."""
    def sub(m):
        return f"![{m.group(1)}]({rewrite_img_src(m.group(2), ch)})"
    text = re.sub(r"</?details\b[^>]*>|</?summary>", "", text)
    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", sub, text)


def parse_blocks(lines, ch):
    """Line-based state machine -> typed blocks."""
    blocks = []
    i, n = 0, len(lines)
    para = []

    def flush_para():
        nonlocal para
        if para:
            text = inline_clean("\n".join(para).strip(), ch)
            if text:
                blocks.append({"t": "p", "text": text})
            para = []

    def flush_math_chunk(chunk):
        tex = "\n".join(chunk).strip()
        if tex:
            blocks.append({"t": "math", "tex": tex})

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # fenced code (no language tags in these sources)
        if stripped.startswith("```"):
            flush_para()
            i += 1
            code = []
            while i < n and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1  # closing fence
            blocks.append({"t": "code", "text": "\n".join(code).rstrip()})
            continue

        # <details> collapsible (worked solutions) — the opener may carry
        # attributes (`<details open>`) and an inline <summary> (single-line
        # form) or a standalone summary line
        m_det = re.match(r"^<details\b[^>]*>", stripped)
        if m_det:
            flush_para()
            is_open = re.match(r"^<details\b[^>]*\bopen\b", stripped) is not None
            summary = "Solution"
            m0 = re.search(r"<summary>(.*?)</summary>", stripped)
            if m0:
                summary = re.sub(r"[^A-Za-z0-9 &'/-]+", " ", m0.group(1)).strip() or "Solution"
            i += 1
            inner = []
            depth = 1
            while i < n:
                s2 = lines[i].strip()
                if re.match(r"^<details\b", s2):
                    depth += 1
                if s2.startswith("</details>"):
                    depth -= 1
                    if depth == 0:
                        i += 1
                        break
                m = re.match(r"<summary>(.*?)</summary>\s*$", s2)
                if m:
                    summary = re.sub(r"[^A-Za-z0-9 &'/-]+", " ", m.group(1)).strip() or "Solution"
                elif not s2.startswith("<summary>"):
                    inner.append(lines[i])
                i += 1
            det = {"t": "details", "summary": summary, "blocks": parse_blocks(inner, ch)}
            if is_open:
                det["open"] = True
            blocks.append(det)
            continue
        if stripped.startswith("<summary>"):
            i += 1
            continue

        # section-divider headings (module-split mode keeps interior ## / # lines)
        if stripped.startswith("## "):
            text = stripped[3:].strip()
            if re.match(r"(master )?table of contents$", text, re.IGNORECASE):
                i += 1
                continue
            flush_para()
            blocks.append({"t": "h2", "text": text})
            i += 1
            continue
        if stripped.startswith("# "):
            text = stripped[2:].strip()
            if re.match(r"table of contents$", text, re.IGNORECASE):
                i += 1
                continue
            flush_para()
            blocks.append({"t": "h2", "text": text})
            i += 1
            continue

        # GitHub alert callout (optional inline title: > [!NOTE] My title);
        # fenced ASCII diagrams inside the callout become code blocks between
        # alert fragments
        m = re.match(r">\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*(.*)$", stripped, re.IGNORECASE)
        if m:
            flush_para()
            i += 1
            alert_type = m.group(1).upper()
            title = m.group(2).strip() or None
            body = []

            def flush_alert():
                text = inline_clean("\n".join(body).strip(), ch)
                body.clear()
                if text:
                    blocks.append({"t": "alert", "type": alert_type, "title": title, "text": text})

            while i < n and lines[i].lstrip().startswith(">"):
                s2 = re.sub(r"^\s*>\s?", "", lines[i])
                st2 = s2.strip()
                if st2.startswith("```"):
                    flush_alert()
                    i += 1
                    code = []
                    while i < n:
                        t2 = re.sub(r"^\s*>\s?", "", lines[i]).strip()
                        if t2.startswith("```"):
                            i += 1
                            break
                        code.append(re.sub(r"^\s*>\s?", "", lines[i]))
                        i += 1
                    blocks.append({"t": "code", "text": "\n".join(code).rstrip()})
                    continue
                mm = re.match(r"<summary>(.*?)</summary>\s*$", st2)
                if mm:
                    title = re.sub(r"[^A-Za-z0-9 &'/-]+", " ", mm.group(1)).strip() or "Solution"
                elif not st2.startswith("<summary>"):
                    body.append(s2)
                i += 1
            flush_alert()
            continue

        # plain blockquote (none expected, be safe)
        if stripped.startswith(">"):
            flush_para()
            body = []
            while i < n and lines[i].lstrip().startswith(">"):
                body.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            blocks.append({"t": "p", "text": inline_clean("\n".join(body).strip(), ch)})
            continue

        # table
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            flush_para()
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                cells = split_table_row(lines[i])
                rows.append(cells)
                i += 1
            header, align, data = rows[0], rows[1], rows[2:]
            # normalize ragged rows to the header width: pad short rows, merge
            # overflow cells into the last cell (OCR-mangled separators keep
            # all their text; the pipes render literally inside that cell)
            ncols = len(header)
            norm = []
            for r in data:
                if len(r) < ncols:
                    r = r + [""] * (ncols - len(r))
                elif len(r) > ncols:
                    r = r[:ncols - 1] + [" | ".join(r[ncols - 1:])]
                norm.append(r)
            blocks.append({"t": "table", "header": [inline_clean(c, ch) for c in header],
                           "align": align, "rows": [[inline_clean(c, ch) for c in r] for r in norm]})
            continue

        # display math $$ ... $$ (single-line or multi-line); the opening line may
        # be bullet-prefixed (`* $$…`) inside list items — strip the marker first
        math_src = re.sub(r"^[-*]\s+", "", stripped)
        if math_src.startswith("$$"):
            flush_para()
            # single-line form: `$…$$ trailing text` — keep trailing text
            # (e.g. `$\checkmark$ …`) as a following paragraph, never inside
            # the tex; a pure-quote trail is peeled like the old behaviour
            m2 = re.match(r"\$\$(.*?)\$\$(.*)$", math_src, re.DOTALL)
            if m2:
                trail = m2.group(2).strip().strip('"').strip()
                blocks.append({"t": "math", "tex": m2.group(1).strip().strip('"').strip()})
                if trail:
                    blocks.append({"t": "p", "text": inline_clean(trail, ch)})
                i += 1
                continue
            chunk = [math_src.lstrip("$").strip()]
            i += 1
            trail = ""
            while i < n and "$$" not in lines[i]:
                chunk.append(lines[i])
                i += 1
            if i < n:
                tail_line = lines[i].strip()
                k = tail_line.find("$$")
                chunk.append(tail_line[:k].strip().strip('"'))
                trail = tail_line[k + 2:].strip().strip('"').strip()
                i += 1
            flush_math_chunk(chunk)
            if trail:
                blocks.append({"t": "p", "text": inline_clean(trail, ch)})
            continue

        # images (own line)
        m = IMG_RE.match(stripped)
        if m:
            flush_para()
            blocks.append({"t": "img", "src": rewrite_img_src(m.group(2), ch), "alt": m.group(1)})
            i += 1
            continue

        # headings
        if stripped.startswith("### "):
            flush_para()
            blocks.append({"t": "h3", "text": stripped[4:].strip()})
            i += 1
            continue
        if stripped.startswith("#### "):
            flush_para()
            blocks.append({"t": "h4", "text": stripped[5:].strip()})
            i += 1
            continue
        # deeper levels (##### / ######) render as h4 — the sources use them for
        # per-problem sub-headings and literal hashes would leak into p blocks
        m = re.match(r"^#{5,6}\s+(.*)$", stripped)
        if m:
            flush_para()
            blocks.append({"t": "h4", "text": m.group(1).strip()})
            i += 1
            continue

        # unordered / ordered lists
        m = re.match(r"^[-*]\s+(.*)$", stripped)
        if m:
            flush_para()
            items = []
            while i < n:
                m2 = re.match(r"^[-*]\s+(.*)$", lines[i].strip())
                if not m2:
                    break
                item = re.sub(r"^\[( |x)\]\s*", lambda mm: "✓ " if mm.group(1) == "x" else "◻ ", m2.group(1).strip())
                items.append(inline_clean(item, ch))
                i += 1
            blocks.append({"t": "ul", "items": items})
            continue
        m = re.match(r"^(\d+)[.)]\s+(.*)$", stripped)
        if m:
            flush_para()
            start = int(m.group(1))
            items = []
            while i < n:
                m2 = re.match(r"^(\d+)[.)]\s+(.*)$", lines[i].strip())
                if not m2:
                    break
                items.append(inline_clean(m2.group(2).strip(), ch))
                i += 1
            # display math often interleaves numbered items — each fragment
            # becomes its own ol block, so preserve the original start number
            blocks.append({"t": "ol", "start": start, "items": items})
            continue

        # horizontal rules / blanks
        if re.match(r"^-{3,}\s*$", stripped) or stripped == "":
            flush_para()
            i += 1
            continue

        para.append(line)
        i += 1

    flush_para()
    return blocks


def build_chapter(ch):
    # file inventory of the chapter's figure folder (or the folder referenced
    # by sheet chapters via figures_ref) — drives the .svg-twin preference in
    # rewrite_img_src
    figdir = ch.get("figures_src") or ch.get("figures_ref")
    ch["_fig_files"] = set(os.listdir(figdir)) if figdir and os.path.isdir(figdir) else set()
    raw = open(ch["md"], encoding="utf-8").read().replace("\r\n", "\n")
    # per-chapter source typo repairs (sources stay read-only; exact matches)
    for bad, good in REPAIRS.get(ch["id"], []):
        raw = raw.replace(bad, good)
    # OCR corruption repair: LaTeX escapes \a \b \t \v \f \r sometimes survive
    # the MD export as literal control chars (BEL, BS, TAB, VT, FF, CR).
    # Restore each to backslash + macro letter when followed by a lowercase
    # letter (FF+"rac" -> \frac, CR+"ight" -> \right).
    CTRL_MAP = {"\a": "a", "\b": "b", "\t": "t", "\v": "v", "\f": "f", "\r": "r"}
    raw = re.sub("[\x07\x08\x09\x0b\x0c\x0d](?=[a-z])",
                 lambda m: "\\" + CTRL_MAP[m.group(0)], raw)
    # drop the MD's own TOC: the `## Table of Contents` section (entries are
    # internal-anchor link lines — some TOCs are followed by H1 headers, so
    # stop at any H1/H2) and a bare `# Table of Contents` h1. The "Master"
    # variant heading (sheet-style TOCs in the Masters) is dropped as a line;
    # its entries fall to the anchor dropper below.
    raw = re.sub(r"^# Table of Contents\s*$", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"^## [^#\n]*Table of Contents\s*$.*?(?=^## |^# )",
                 "", raw, flags=re.MULTILINE | re.DOTALL)
    # safety net: surviving internal-anchor link lines (TOC remnants), numbered
    # or bullet-prefixed
    raw = re.sub(r"(?m)^\s*(?:[-*]\s*)?(?:\d+[.)]\s*)?\[[^\]]*\]\(#[^)]+\)\s*$", "", raw)
    # repair hard-wrapped headings / bold / math / table rows — new-format
    # sources only (Ch4-7 Masters, sheets Ch4-7, Network Theory); the older
    # chapters are stable and must stay byte-identical
    if ch.get("unwrap"):
        raw = "\n".join(unwrap_lines(raw.split("\n")))

    # gallery tables / list items referencing the 4K blueprint JPGs as
    # `[text](file:///...)` links are dead on the site — rewrite them into
    # standalone figure blocks (Network Theory / Analog Electronics sources)
    if ch.get("fig_links"):
        raw = convert_fig_links(raw)

    # section splitting: generic chapters split at every `## `; module-split
    # chapters (audit-concatenated Masters) split only at Module headers at ANY
    # heading level (Ch1 uses `## Module N:`, Ch2 uses `# Module N:`) and keep
    # interior ## / # lines as divider blocks via parse_blocks; section-split
    # chapters (Formula & Revision Sheets) split at `Section N:` headers; the
    # Network Theory Masters are H1-partitioned (title/subtitle, then one H1
    # per part) — their file-top H1s are blanked so the metadata blockquote +
    # blueprint gallery become the About section.
    mode = ch.get("section_split", "h2")
    if mode == "module":
        split_re = r"^#{1,6} (?=Module )"
    elif mode == "section":
        split_re = r"^#{1,6} (?=Section )"
    elif mode == "part":
        # Roman-numeral parts only — drill sub-parts (`Part (a):`, `Part 1:`)
        # must not split
        split_re = r"^#{1,6} (?=Part (?:X|IX|VIII|VII|VI|V|IV|III|II|I)[:\s(])"
    elif mode == "h1":
        split_re = r"^# +"
        head = raw.split("\n")
        j = 0
        while j < len(head) and head[j].startswith("# "):
            head[j] = ""
            j += 1
        raw = "\n".join(head)
    else:
        split_re = r"^## +"
    parts = re.split(split_re, raw, flags=re.MULTILINE)
    sections = []
    if parts[0].strip():
        pre_text = parts[0].strip()
        if mode == "section":
            # formula sheets carry a huge `## Master Table of Contents` at the
            # end of the preamble — drop it wholesale; the app renders its own
            # TOC sidebar, and the sheet's sub-entries are plain text lines
            # the anchor-line dropper cannot catch
            toc_i = pre_text.find("## Master Table of Contents")
            if toc_i != -1:
                pre_text = pre_text[:toc_i]
        pre_lines = pre_text.split("\n")
        # drop the h1 title itself (module metadata already carries it)
        pre_blocks = parse_blocks([l for l in pre_lines if not l.startswith("# ")], ch)
        if pre_blocks:
            sections.append({"id": "about", "title": "About this chapter", "blocks": pre_blocks})
    for part in parts[1:]:
        lines = part.split("\n")
        title = clean_title(lines[0].strip())
        if not title:
            continue
        sid = slugify(lines[0].strip())
        body = parse_blocks(lines[1:], ch)
        if not body:
            continue
        sections.append({"id": sid, "title": title, "blocks": body})

    module = {
        "id": ch["id"],
        "num": ch["num"],
        "part": ch.get("part"),
        "title": ch["title"],
        "subject": ch["subject"],
        "source": os.path.basename(ch["md"]),
        "generatedAt": datetime.date.today().isoformat(),
        "sections": sections,
    }
    return module


def write_module(module, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fp:
        fp.write("// GENERATED by scripts/build_notes.py — do not hand-edit.\n")
        fp.write(f"// Source: {module['source']} · generated {module['generatedAt']}\n")
        fp.write(f"export default {json.dumps(module, ensure_ascii=True, indent=1)};\n")


def main():
    index = {}
    for ch in CHAPTERS:
        module = build_chapter(ch)
        nblocks = sum(len(s["blocks"]) for s in module["sections"])
        out = os.path.join(BASE, "src", "data", "notes", ch["notes_sub"], f"{ch['file']}.js")
        write_module(module, out)
        index[module["id"]] = {
            "num": module["num"],
            "title": module["title"],
            "subject": module["subject"],
            "sections": [{"id": s["id"], "title": s["title"]} for s in module["sections"]],
        }
        # figures (png/jpg/jpeg)
        if ch["figures_src"] and os.path.isdir(ch["figures_src"]):
            dst = os.path.join(BASE, "public", *ch["figures_dst"].split("/"))
            os.makedirs(dst, exist_ok=True)
            copied = 0
            for f in os.listdir(ch["figures_src"]):
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".svg")):
                    shutil.copy2(os.path.join(ch["figures_src"], f), os.path.join(dst, f))
                    copied += 1
            print(f"  figures: copied {copied} images -> public/{ch['figures_dst']}")
        print(f"{module['id']}: {len(module['sections'])} sections, {nblocks} blocks -> {os.path.relpath(out, BASE)}")

    idx_path = os.path.join(BASE, "src", "data", "notes", "index.js")
    with open(idx_path, "w", encoding="utf-8", newline="\n") as fp:
        fp.write("// GENERATED by scripts/build_notes.py — do not hand-edit.\n")
        fp.write("// Lightweight per-chapter section index (course page accordion + search).\n")
        fp.write(f"export const NOTES_INDEX = {json.dumps(index, ensure_ascii=True, indent=1)};\n")
    print(f"index -> {os.path.relpath(idx_path, BASE)}")


if __name__ == "__main__":
    main()
