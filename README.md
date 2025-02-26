# Growth Mindset Journey App

A comprehensive web application built with Streamlit that helps users cultivate a growth mindset through data analysis, goal tracking, reflection journaling, and skill development visualization.

## What is a Growth Mindset?

A growth mindset is the belief that your abilities and intelligence can be developed through dedication, hard work, and learning from feedback. This concept was popularized by psychologist Carol Dweck and contrasts with a fixed mindset, which believes abilities are static traits.

With a growth mindset, you:
- Embrace challenges as opportunities to learn
- Persist in the face of obstacles
- See effort as a path to mastery
- Learn from criticism and feedback
- Find inspiration in the success of others

## Features

This application includes:

1. **Data Analysis Tools**
   - Upload and analyze CSV or Excel files
   - Clean data (remove duplicates, handle missing values)
   - Visualize data with multiple chart types
   - Export processed data in various formats

2. **Learning Goals Tracker**
   - Set and track specific learning goals
   - Monitor progress with visual indicators
   - Organize goals by category
   - Define milestones for each goal

3. **Reflection Journal**
   - Document your learning journey
   - Analyze reflection patterns
   - Foster growth mindset thinking
   - Track growth mindset metrics over time

4. **Skill Development Tracker**
   - Visualize your skills with radar charts
   - Track skill progress over time
   - Set target skill levels
   - Document resources for improvement

## Installation

1. Clone this repository:
```
git clone <repository_url>
cd growth_mindset_app
```

2. Create a virtual environment (recommended):
```
python -m venv venv
```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. Install the required packages:
```
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:
```
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Use the sidebar to navigate between different sections of the app

## Data Privacy

All data is stored locally in your browser's session state. No data is sent to external servers. When you close your browser, the data will be cleared unless you export it.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Carol Dweck for her pioneering research on growth mindset
- The Streamlit team for creating such a powerful framework for building data apps
- The Python community for developing and maintaining the libraries used in this project 