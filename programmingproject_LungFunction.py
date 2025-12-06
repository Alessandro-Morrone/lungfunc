import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import animation
DATAFILE = r"C:\Users\gmorr\OneDrive\Desktop\Programming_Project_Data_REALSheet1.csv"      #/Users/uzma/Desktop/Programming_Project_Data_REAL(Sheet1).csv
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
    plt.figure(figsize=(7,4))
    sns.lineplot(data=df, x="Time", y="Volume", hue="PatientID", legend=False)
    plt.title("Volume-Time Curve")
    plt.xlabel("Time (s)")
    plt.ylabel("Volume (L)")
    plt.savefig(r"volume_time_curve.png")
    plt.show()
    plt.close()

 # Flow-Volume curve
    plt.figure(figsize=(7,4))
    sns.lineplot(data=df, x="Volume", y="Flow", hue="PatientID", legend=False)
    plt.title("Flow-Volume Curve")
    plt.xlabel("Volume (L)")
    plt.ylabel("Flow (L/s)")
    plt.savefig(r"flow_volume_curve.png")
    plt.show()
    plt.close()

    # Histogram of FEV1
    plt.figure(figsize=(7,5))
    sns.histplot(data=metrics, x="FEV1", bins=10, kde=True)
    plt.title("Histogram of FEV1")
    plt.xlabel("FEV1 (L)")
    plt.savefig(r"hist_fev1.png")
    plt.show()
    plt.close()

    #boxplot of FEV1/FVC
    plt.figure(figsize=(6,4))
    sns.boxplot(data=metrics, y="FEV1_FVC")
    plt.title("Boxplot of FEV1/FVC Ratio")
    plt.ylabel("FEV1/FVC")
    plt.savefig(r"box_fev1_fvc.png")
    plt.show()
    plt.close()

    # make animation (function code is missing here)

def animate_breathing(df, patient_id):
    patient_data= df[df["PatientID"] == patient_id]
    t = patient_data["Time"].values
    v = patient_data["Volume"].values

    fig, ax = plt.subplots(figsize=(6,4))
    ax.set_xlim(min(t), max(t))
    ax.set_ylim(min(v), max(v))
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("volume (L)")
    ax.set_title(f"Breathing Curve Over time - {patient_id}")

    line, = ax.plot([], [], lw=2)
    print(line)

    def animate(i):
        x = t[:i]
        y = v[:i]
        line.set_data(x,y)
        return line, 

    anim = animation.FuncAnimation(fig, animate, frames=len(t), interval = 200)
    plt.show()
    anim.save(f"{patient_id}_breathing_animation.mp4")


    
def export_summary(metrics):
    metrics.to_csv("Lung_summary.csv", index=False)

if __name__ == "__main__":
    df = load_data(DATAFILE)  
    print(df)          
    metrics = compute_lung_metrics(df)
    print(metrics)

    create_plots(metrics, df)
    export_summary(metrics)
    animate_breathing(df, "P01")