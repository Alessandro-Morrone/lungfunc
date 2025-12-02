import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import animation
DATAFILE = r"/Users/uzma/Desktop/Programming_Project_Data_REAL(Sheet1).csv"
def load_data(path):
    df = pd.read_csv(path)
    df = df[['PatientID', 'Time', 'Volume', 'Flow']]
    df = df.dropna(subset=['PatientID', 'Time', 'Volume', 'Flow'])
    return(df)

def compute_lung_metrics(df):
   metrics_list = []
   # Loop over each patient
   for patient in df['PatientID'].unique():
        patient_data = df[df['PatientID'] == patient]

        # FEV1: max volume at or before 1 second
        fev1 = patient_data[patient_data['Time'] <= 1]['Volume'].max()

        # FVC: total volume exhaled
        fvc = patient_data['Volume'].max()

        # FEV1/FVC ratio
        ratio = fev1 / fvc if fvc != 0 else np.nan

        # PEF: peak expiratory flow
        pef = patient_data['Flow'].max()

        # Append results
        metrics_list.append([patient, fev1, fvc, ratio, pef])

    # Convert to DataFrame
        metrics_df = pd.DataFrame(
        metrics_list,
        columns=['PatientID', 'FEV1', 'FVC', 'FEV1_FVC', 'PEF']
    )
        return metrics_df  # <--- MUST return!

def create_plots(metrics, df):
# Volume-Time curve
    plt.figure(figsize=(6,4))
    sns.lineplot(data=df, x="Time (seconds)", y="Volume (L)", hue="SiteID")
    plt.title("Volume-Time Curve")
    plt.savefig(r"")
    plt.close()

 # Flow-Volume curve
    plt.figure(figsize=(8,4))
    sns.lineplot(data=df, x="Volume (L)", y="Flow (L/s)", hue="SiteID")
    plt.title("Flow-Volume Curve")
    plt.savefig(r"")
    plt.close()

    # Histogram of FEV1
    plt.figure(figsize=(7,5))
    sns.histplot(df.corr(numeric_only=True), annot=True, cmap="coolwarm", bins=10)
    plt.title("Histogram of FEV1")
    plt.savefig(r"")
    plt.close()

    #boxplot of FEV1/FVC
    plt.figure(figsize=(6,4))
    sns.boxplot(data=df, x="", y="FEV1/FVC ratio")
    plt.title("Box Plot of FEV1/FVC Ratios")
    plt.savefig(r"")
    plt.close()

    # make animation (function code is missing here)

def animate_breathing(df):
    g

def export_summary(df):
    df.to_csv(r"C:\Users\2473732\Desktop\Lung_summary.csv", index=False)

if __name__ == "__main__":
    df = load_data(DATAFILE)  
    print(df.head())          
    metrics = compute_lung_metrics(df)
    print(metrics.head())
