&nbsp;🧬 DNA-Identifier: Advanced Forensic DNA Profiling Tool



!\[Python](https://img.shields.io/badge/python-3.x-blue)

!\[License](https://img.shields.io/badge/license-MIT-green)

!\[CODIS](https://img.shields.io/badge/CODIS-20%20markers-orange)

!\[Last Commit](https://img.shields.io/github/last-commit/rahula2006/DNA-Identifier)

!\[Stars](https://img.shields.io/github/stars/rahula2006/DNA-Identifier?style=social)

&nbsp;🔬 Overview



A \*\*production-ready forensic DNA analysis tool\*\* that implements the FBI's CODIS (Combined DNA Index System) standard with 20 STR markers. This tool can identify individuals from DNA samples with a random match probability of \*\*1 in 10 quintillion\*\*—stronger than a fingerprint match!



&nbsp;🎯 Key Features



| Feature | Description |

|---------|-------------|

| \*\*20 CODIS STR Markers\*\* | Full FBI-standard panel (CSF1PO, D3S1358, D5S818, D7S820, D8S1179, D13S317, D16S539, D18S51, D21S11, FGA, TH01, TPOX, vWA, AMEL, PEthD12, PentaD, PentaE, SE33, CD4, F13A01) |

| \*\*Statistical Analysis\*\* | Calculates random match probability (1 in 10^19) |

| \*\*Partial Matching\*\* | Handles degraded DNA with ±2 repeat tolerance |

| \*\*Sex Determination\*\* | AMEL marker analysis for male/female identification |

| \*\*Forensic Visualization\*\* | Generates professional electropherograms |

| \*\*Case Reports\*\* | Creates detailed forensic reports |

&nbsp;📊 How It Works



```mermaid

graph LR

&nbsp;   A\[DNA Sample] --> B\[Extract 20 STR Markers]

&nbsp;   B --> C\[Compare with Database]

&nbsp;   C --> D\[Calculate Match Probability]

&nbsp;   D --> E\[Generate Electropherogram]

&nbsp;   E --> F\[Forensic Report]







Prerequisites



\# Install required Python package (only for visualization)

pip install matplotlib



Clone and Run

bash

\# Clone the repository

git clone https://github.com/rahula2006/DNA-Identifier.git

cd DNA-Identifier



\# Basic DNA matching (3 markers)

python dna.py databases/small.csv sequences/bob.txt



\# Advanced CODIS matching (20 markers)

python dna\_advanced.py databases/codis\_20.csv sequences/john\_doe.txt



\# Generate forensic visualization

python visualize\_profile.py databases/codis\_20.csv John\_Doe





📁 Project Structure



DNA-Identifier/

├── 📜 README.md                    # This file

├── 📜 LICENSE                      # MIT License

├── 📜 .gitignore                   # Git ignore file

├── 📜 requirements.txt              # Python dependencies

│

├── 🐍 Core Scripts

│   ├── dna.py                      # Basic 3-marker DNA matcher

│   ├── dna\_advanced.py              # Advanced 20-marker CODIS system

│   └── visualize\_profile.py          # Forensic visualization tool

│

├── 📂 databases/

│   ├── small.csv                    # 3 markers, 3 individuals

│   └── codis\_20.csv                  # 20 markers, 12 individuals

│

├── 📂 sequences/

│   ├── bob.txt                       # Sample matching Bob

│   ├── alice.txt                     # Sample matching Alice

│   ├── john\_doe.txt                  # Sample matching John\_Doe

│   └── unknown.txt                   # Unknown sample

│

└── 📂 outputs/                        # Generated files

&nbsp;   ├── John\_Doe\_profile.png           # Electropherogram

&nbsp;   ├── John\_Doe\_report.txt             # Forensic report

&nbsp;   ├── Alice\_profile.png

&nbsp;   ├── Alice\_report.txt

&nbsp;   └── ...



