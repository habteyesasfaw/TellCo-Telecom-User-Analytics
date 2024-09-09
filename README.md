
# TellCo Telecom Data Analysis

This repository contains the analysis of TellCo's telecommunication data to identify growth opportunities and support a potential investment decision. The analysis focuses on user behavior and engagement, providing insights that will guide business strategy and operational improvements.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Task 1: User Overview Analysis](#task-1-user-overview-analysis)
  - [Subtasks](#subtasks)
- [Task 2: User Engagement Analysis](#task-2-user-engagement-analysis)
  - [Subtasks](#subtasks)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project analyzes a dataset provided by TellCo, a mobile service provider in the Republic of Pefkakia. The objective is to help a potential investor determine whether purchasing TellCo would be a worthwhile investment by analyzing customer behavior and engagement.

The analysis is divided into two main tasks:
- **Task 1**: User Overview Analysis
- **Task 2**: User Engagement Analysis

## Project Structure

```
.
├── data/                          # Raw and processed data
├── notebooks/                     # Jupyter notebooks for analysis
├── scripts/                       # Python scripts for analysis
├── src/                           # Utility functions
├── README.md                      # Project documentation
└── requirements.txt               # Dependencies
```

## Task 1: User Overview Analysis

In this task, we conduct a user overview analysis to understand customer behavior, specifically focusing on handsets used and user activity on applications like social media, Google, YouTube, Netflix, etc.

### Subtasks

- Identify the top 10 handsets used by customers.
- Identify the top 3 handset manufacturers and their top 5 handsets.
- Aggregate data per user on xDR sessions, session duration, total download/upload data, and total session data volume for each application.
- Explore missing values, outliers, and apply necessary data treatments.

## Task 2: User Engagement Analysis

This task focuses on analyzing user engagement with different applications based on metrics like session frequency, session duration, and total traffic.

### Subtasks

- Track top 10 customers by engagement metrics.
- Normalize metrics and perform k-means clustering to classify users into engagement groups.
- Visualize user engagement and analyze the most used applications.

## Technologies Used

- **Python**: Core programming language for data analysis
- **Pandas**: Data manipulation and analysis
- **Matplotlib** & **Seaborn**: Data visualization
- **Scikit-learn**: Machine learning for clustering
- **PostgreSQL**: Database for querying telecom data
- **Jupyter Notebook**: For exploratory analysis

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tellco-telecom-analysis.git
   cd tellco-telecom-analysis
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL connection in `src/utils.py`:
   ```python
   db = PostgresConnection(dbname='telecom', user='your_user', password='your_password', host='localhost', port='5432')
   db.connect()
   ```

## Usage

### Jupyter Notebooks

The analysis can be run through Jupyter notebooks located in the `notebooks/` directory:
- **Task 1**: `Telecom_User_Overview.ipynb`
- **Task 2**: `Telecom_User_Engagement.ipynb`

### Python Scripts

You can also run the analysis using the provided scripts in the `scripts/` directory:
```bash
python scripts/user_engagement_analysis.py
```

## Results

- Insights into the most popular handsets and applications used by TellCo customers.
- Identification of the most engaged users based on session metrics.
- Recommendations for marketing and network optimization based on user behavior.

## Contributing

Feel free to contribute by submitting a pull request. For major changes, please open an issue to discuss what you'd like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

