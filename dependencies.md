# Project Dependencies

These are the Python packages required for this athlete monitoring platform:

```
streamlit==1.27.0
pandas==2.0.3
numpy==1.24.3
plotly==5.16.0
scikit-learn==1.3.0
scipy==1.11.2
joblib==1.3.2
pytz==2023.3
streamlit-extras==0.3.2
```

## Installation Commands

To install these dependencies using pip, run:

```bash
pip install -r requirements.txt
```

If you need to install them individually:

```bash
pip install streamlit pandas numpy plotly scikit-learn scipy joblib pytz streamlit-extras
```

## Running the Application

To run the Streamlit application, use:

```bash
streamlit run app.py --server.port 5000
```

This will start the application on port 5000, making it accessible at `http://localhost:5000`.

## Additional Notes

- Make sure you have Python 3.9+ installed
- For development, you might want to use a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```
- Some visualization components may require additional JavaScript libraries, but Streamlit handles these dependencies automatically