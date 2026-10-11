# Campus Lost and Found Matcher

 📌 Project Overview

Campus Lost and Found Matcher is a Python-based application designed to help students report lost and found items on campus. It compares reports using item descriptions, categories, locations, and dates to suggest possible matches.

## 🎯 Objectives

- Make it easier to report lost and found items.
- Help users identify potentially matching reports.
- Rank possible matches using a simple scoring algorithm.
- Reduce irrelevant matches by ignoring common words.
- Maintain report statuses such as Reported, Matched, and Returned.

## ✨ Features

- Add lost and found reports.
- Search reports by category or description.
- Suggest possible matches between lost and found items.
- Calculate match scores based on report details.
- Ignore common words while comparing descriptions.
- Compare the original and improved matching algorithms using 10 sample reports.
- Update report status.
- Store report data locally in JSON format.

## 🛠️ Technologies Used

- Python
- Regular Expressions
- JSON
- Git and GitHub

## 🧠 Matching Algorithm

The application considers:

1. **Same category:** Adds a base score.
2. **Shared meaningful words:** Adds points for words shared between descriptions.
3. **Same location:** Adds additional points.
4. **Nearby dates:** Adds points when report dates are within three days.

The improved algorithm ignores common words such as "the", "a", and "is" when comparing descriptions.

The highest-scoring eligible reports are displayed first. A suggested match is only a candidate and does not prove ownership.

## ▶️ How to Run

### Prerequisites

- Python 3 installed
- Git (optional, for version control)

### Steps

1. Download or clone this repository.
2. Open the project folder in a terminal.
3. Run the application:

   ```bash
   python Lost_found/app.py
   ```

4. Open the local address displayed by the application in your browser, if it does not open automatically.

## 📁 Project Structure

```text
daa_project_assignment/
├── common.py
├── README.md
└── Lost_found/
    ├── app.py
    └── data.json
```

**Note:** `data.json` stores local report data and may be created automatically by the application. Do not upload private or personal information.

## 🧪 Testing

The application includes a comparison of the original and improved matching algorithms using 10 sample reports. This allows their match scores to be compared.

## 🚀 Future Enhancements

- Improve matching using more advanced text similarity techniques.
- Add user authentication.
- Provide notifications for possible matches.
- Develop a database-backed version.

## 👩‍💻 Project Information

**Project:** Campus Lost and Found Matcher  
**Domain:** Design and Analysis of Algorithms (DAA)  
**Language:** Python
