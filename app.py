from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)


@app.route('/')
def dashboard():
    # Sample data
    data = {'Category': ['A', 'B', 'C', 'D'], 'Values': [23, 45, 12, 37]}
    df = pd.DataFrame(data)

    # Plotting the data
    plt.figure(figsize=(6, 4))
    plt.bar(df['Category'], df['Values'], color='skyblue')
    plt.title('Sample Bar Chart')
    plt.xlabel('Category')
    plt.ylabel('Values')

    # Save plot to a string
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('Dashboard.html', plot_url=plot_url)


if __name__ == '__main__':
    app.run(debug=True)