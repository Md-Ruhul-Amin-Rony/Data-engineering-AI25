# Data Engineering AI25

Welcome to the Data Engineering course, part of Utvecklare inom AI och maskininlärning at IT-Högskolan. This repo contains lecture slides, code, and exercises for the course.

The aim of this course is to learn data engineering concepts both theoretically and hands-on: building pipelines, orchestrating them, modeling and transforming data, and deploying the result to the cloud. Data engineering is what lets roles like data scientists and ML engineers work with clean, reliable, well-structured data instead of worrying about how it got there. The course closes with a group project in which you train (using skills from other courses in the program), deploy, and monitor a real AI model in the cloud, built using an agile (Scrum/Kanban) process.

This course builds on prior skills in:

- Python, Pandas, Numpy, SQL
- Data visualisation (matplotlib, seaborn, plotly)
- Git and GitHub (a refresher is given in Week 2)

Repo structure
.
├── .devcontainer/       # GitHub Codespaces environment — see below
├── lectures/
│   ├── theory/          # Lecture slides, as PDFs
│   └── code/            # Per-lecture code examples and exercises
├── resources/            # Extra reading per week
└── README.md


Week	Teaching days (Tue/Thu)	Lecture(s) used
1	11/8, 13/8	Lecture1.1 (course structure), Lecture1.2 (DE intro), Lecture1.3 (Bash), Lecture2.1 (Docker)
2	18/8, 20/8	Lecture3.1 (Git), Lecture4.1 (data workflow)
3	25/8, 27/8	Lecture5.1 (Airflow) + new material (medallion architecture, DuckDB, warehouse landscape)
4	1/9, 3/9	Lecture7.1 (recap), Lecture8.1 (agile: Scrum + Kanban)
5	8/9, 10/9	Lecture9.1 (cloud) + new material (Kubernetes/AKS); project kickoff
6	15/9, 17/9	New material (Hopsworks feature store); project work
7	22/9, 24/9	Lecture11.1 (CI/CD) + new material (data quality, monitoring); project work
8	29/9, 1/10	Lecture13.1 (SCD), Lecture14.1 (security/GDPR), Lecture15.1 (dbt) + new material (Databricks, PySpark, broadened ethics); project work
9	6/10, 8/10	Project presentation, report, wrap-up

Dev environment: GitHub Codespaces

Everyone develops in a browser-based GitHub Codespace — no local installs, which matters since most students use school-provided Windows laptops without admin rights.

Open this repo on github.com → Code → Codespaces → Create codespace on main. The .devcontainer/ config gives you Python 3.12 + uv, Docker-in-Docker, Azure CLI, kubectl + Helm, and matching VS Code extensions (Python, Docker, Kubernetes, Azure Account, Git Graph), with zero manual setup.

Schedule

Tuesdays and Thursdays, 09:00–12:00 and 13:00–15:00, 11 August – 8 October 2026. Office hours/handledning: 3 hours/week (announced separately). Monday/Wednesday/Friday are unsupervised self-study days.

Credits

Original course content by Esoon Ko and, before that, Kokchun Giang, for IT-Högskolan Göteborg. 2026 updates by Mikael Huss.
