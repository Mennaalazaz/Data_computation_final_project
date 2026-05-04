from flask import Flask, request, render_template
import joblib
import pandas as pd
from datetime import datetime  
import json
import plotly
import plotly.express as px
import sys

# 1. DEFINE THE CLEANING FUNCTION , This must match what the model was trained with
def clean_data(X):
    X = X.copy()
    drop_cols = [
        'Unnamed: 0', 'id', 'friends', 'is_starred', 'is_backing', 
        'permissions', 'photo', 'slug', 'urls', 'source_url',
        'creator', 'location', 'category', 'profile',
        'name', 'blurb', 'pledged', 'usd_pledged', 'backers_count',
        'spotlight', 'state_changed_at', 'launch_to_state_change',
        'deadline', 'created_at', 'launched_at',
        'state_changed_at_weekday', 'state_changed_at_month',
        'state_changed_at_day', 'state_changed_at_yr', 'state_changed_at_hr'
    ]
    X = X.drop(columns=[c for c in drop_cols if c in X.columns])
    
    duration_cols = ['create_to_launch', 'launch_to_deadline']
    for col in duration_cols:
        if col in X.columns:
            # Handle duration conversion
            X[col] = pd.to_timedelta(X[col]).dt.total_seconds() / (24 * 60 * 60)
    return X

app = Flask(__name__)

# Manually inject the function into the __main__ namespace so joblib can find it
import __main__
__main__.clean_data = clean_data

# Load data globally
df_all = pd.read_csv('data/kickstarter_data_with_features.csv')

# 2. LOAD THE MODEL
model = joblib.load('EDA_Modeling/kickstarter_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 1. Basic Text and Numeric Inputs
        name = request.form.get('name', '')
        blurb = request.form.get('blurb', '')
        goal = float(request.form.get('goal', 0))
        country = request.form.get('country', 'US')
        staff_pick = int(request.form.get('staff_pick', 0))
        disable_comm = int(request.form.get('disable_communication', 0))
        
        # 2. Currency Inputs 
        currency = request.form.get('currency', 'USD')
        currency_symbol = request.form.get('currency_symbol', '$')
        # Usually boolean/binary in datasets: does it have a trailing code?
        currency_trailing = int(request.form.get('currency_trailing_code', 0))
        # Static rate (conversion to USD, usually 1.0 if already USD)
        static_usd_rate = float(request.form.get('static_usd_rate', 1.0))

        # 3. Parse Dates
        # Format usually comes from HTML datetime-local as 'YYYY-MM-DDTHH:MM'
        launch_dt = datetime.strptime(request.form.get('launched_at'), '%Y-%m-%dT%H:%M')
        deadline_dt = datetime.strptime(request.form.get('deadline'), '%Y-%m-%dT%H:%M')
        created_dt = datetime.now() # Current time as the "creation" time

        # 4. Feature Engineering: Building the Dataframe
        data = {
            # Numerical
            'goal': [goal],
            'static_usd_rate': [static_usd_rate],
            'name_len': [len(name)],
            'name_len_clean': [len(name.strip())],
            'blurb_len': [len(blurb)],
            'blurb_len_clean': [len(blurb.strip())],
            
            # Categorical / Identifiers
            'disable_communication': [disable_comm],
            'country': [country],
            'currency': [currency],
            'currency_symbol': [currency_symbol],
            'currency_trailing_code': [currency_trailing],
            'staff_pick': [staff_pick],

            # Launched Date Features
            'launched_at_day': [launch_dt.day],
            'launched_at_yr': [launch_dt.year],
            'launched_at_hr': [launch_dt.hour],
            'launched_at_month': [launch_dt.month],
            'launched_at_weekday': [launch_dt.weekday()],

            # Deadline Date Features
            'deadline_day': [deadline_dt.day],
            'deadline_yr': [deadline_dt.year],
            'deadline_hr': [deadline_dt.hour],
            'deadline_month': [deadline_dt.month],
            'deadline_weekday': [deadline_dt.weekday()],

            # Created At Date Features
            'created_at_day': [created_dt.day],
            'created_at_yr': [created_dt.year],
            'created_at_hr': [created_dt.hour],
            'created_at_month': [created_dt.month],
            'created_at_weekday': [created_dt.weekday()],

            # Durations (Calculated in days)
            'create_to_launch': [(launch_dt - created_dt).total_seconds() / 86400],
            'launch_to_deadline': [(deadline_dt - launch_dt).total_seconds() / 86400]
        }

        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # 5. Prediction
        prediction = model.predict(df)
        result = "SUCCESSFUL" if prediction[0] == 1 else "FAILED"
        color = "#a0c95f" if prediction[0] == 1 else "#e74c3c"
        
        return render_template('index.html', 
                                prediction_text=f'Predicted Status: {result}',
                                result_color=color)

    except Exception as e:
        # Useful for debugging which field failed
        print(f"Prediction Error: {e}")
        return render_template('index.html', prediction_text=f"Error: Please ensure all dates and fields are filled.")
    
@app.route('/dashboard')
def dashboard():
    # --- 1. DATA PREPARATION ---
    viz_df = df_all.copy()
    
    # Map states to consistent labels
    status_map = {
        'successful': 'successful', 1: 'successful', 1.0: 'successful',
        'failed': 'failed', 0: 'failed', 0.0: 'failed'
    }
    viz_df['state_label'] = viz_df['state'].map(status_map).fillna('unknown')
    viz_df = viz_df[viz_df['state_label'] != 'unknown']

    # Helper for consistent, clean appearance
    def update_style(fig):
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", size=12, color="#333"),
            margin=dict(l=60, r=40, t=50, b=100) 
        )
        return fig

    # --- 2. CHART 1: SUCCESS RATE BY CATEGORY ---
    cat_success = (viz_df.groupby('category')['state_label']
                .value_counts(normalize=True)
                .unstack()
                .reset_index())
    
    fig1 = px.bar(cat_success, x='category', y='successful', 
                template="plotly_white",
                color_discrete_sequence=['#a0c95f'])
    fig1 = update_style(fig1)

    # --- 3. CHART 2: GOAL VS. PLEDGED  ---
    sample_df = viz_df.sample(n=min(5000, len(viz_df)), random_state=42)
    
    # Filter out zeros for log scale (Plotly can't handle 0 on log scale)
    sample_df = sample_df[(sample_df['goal'] > 0) & (sample_df['pledged'] > 0)]
    
    fig2 = px.scatter(
        sample_df, x="goal", y="pledged", color="state_label",
        labels={"goal": "Goal ($)", "pledged": "Pledged ($)"},
        template="plotly_white", 
        log_x=True, log_y=True,
        color_discrete_map={'successful': '#a0c95f', 'failed': "#ff5f5f"}
    )
    # Make markers highly visible
    fig2.update_traces(marker=dict(size=6, opacity=0.7))
    
    # Success Line: Where Pledged == Goal (diagonal line y=x)
    max_val = max(sample_df['goal'].max(), sample_df['pledged'].max())
    fig2.add_shape(
        type='line', 
        x0=1, y0=1, 
        x1=max_val, y1=max_val, 
        line=dict(color="#333", width=2, dash="dash"),
        name="Break-even line"
    )
    fig2 = update_style(fig2)

    # --- 4. CHART 3: SUCCESS TRENDS (FIXED - NORMAL LINE, NOT ACCUMULATED) ---
    viz_df['launched_at'] = pd.to_datetime(viz_df['launched_at'])
    
    # Group by month and calculate success rate PER MONTH
    monthly_stats = viz_df.groupby(viz_df['launched_at'].dt.to_period('M')).agg({
        'state_label': lambda x: (x == 'successful').sum() / len(x) * 100
    }).reset_index()
    
    # Convert Period to datetime for plotting
    monthly_stats['launched_at'] = monthly_stats['launched_at'].dt.to_timestamp()
    monthly_stats = monthly_stats.sort_values('launched_at')
    monthly_stats.columns = ['launched_at', 'success_rate']

    fig3 = px.line(
        monthly_stats, x='launched_at', y='success_rate',
        labels={'launched_at': 'Launch Date', 'success_rate': 'Success Rate (%)'},
        template="plotly_white", 
        markers=True
    )
    # Style line to look modern
    fig3.update_traces(
        line=dict(color='#a0c95f', width=3), 
        marker=dict(size=6, color="#333")
    )
    fig3.update_yaxes(range=[0, 100])  # Success rate is a percentage
    fig3 = update_style(fig3)

    # --- 5. FORMATTING & RENDER ---
    def format_curr(value):
        if value >= 1_000_000: return f"{value/1_000_000:.1f}M"
        if value >= 1_000: return f"{value/1_000:.1f}K"
        return f"{value:,.0f}"
    
    # --- 6. CHART 4: SUCCESS DISTRIBUTION BY COUNTRY (PIE) ---
    # Filter for only successful projects to see which countries contribute most
    country_success = viz_df[viz_df['state_label'] == 'successful']['country'].value_counts().reset_index()
    country_success.columns = ['country', 'count']

    # To keep the pie chart clean, group smaller countries into "Other"
    top_n = 8
    if len(country_success) > top_n:
        other_count = country_success.iloc[top_n:]['count'].sum()
        country_success = country_success.iloc[:top_n]
        country_success.loc[len(country_success)] = ['Other', other_count]

    fig4 = px.pie(
        country_success, 
        values='count', 
        names='country',
        template="plotly_white",
        hole=0.4,  # Makes it a Donut chart for a modern look
        color_discrete_sequence=px.colors.sequential.Greens_r
    )
    
    fig4 = update_style(fig4)
    fig4.update_traces(textposition='inside', textinfo='percent+label')
    fig4.update_layout(showlegend=False) # Legend is often redundant with labels on a pie

    return render_template(
        'dashboard.html', 
        graphJSON1=json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder), 
        graphJSON2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder), 
        graphJSON3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder),
        graphJSON4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder),
        total_projects=f"{len(viz_df):,}",
        total_categories=viz_df['category'].nunique(),
        min_goal=format_curr(viz_df['goal'].min()),
        max_goal=format_curr(viz_df['goal'].max()),
        min_pledged=format_curr(viz_df['pledged'].min()),
        max_pledged=format_curr(viz_df['pledged'].max())
    )    

if __name__ == '__main__':
    app.run(debug=True)